"""Main Console class - high-level facade for terminal rendering.

This module provides the primary API for StyledConsole, wrapping Rich console
functionality with additional features like terminal detection, frame/banner
rendering, and HTML export capabilities.

Phase 4.4: Refactored to use specialized manager classes (TerminalManager,
ExportManager, RenderingEngine) following the Facade pattern.
"""

from __future__ import annotations

import sys
import warnings
from collections.abc import Iterable
from typing import TYPE_CHECKING, Any, TextIO

from rich.console import Console as RichConsole

from styledconsole.core.context import StyleContext
from styledconsole.core.export_manager import ExportManager
from styledconsole.core.progress import StyledProgress
from styledconsole.core.rendering_engine import RenderingEngine
from styledconsole.core.terminal_manager import TerminalManager
from styledconsole.core.theme import DEFAULT_THEME, THEMES, Theme
from styledconsole.effects.registry import EFFECTS
from styledconsole.effects.spec import EffectSpec
from styledconsole.policy import RenderPolicy, get_default_policy
from styledconsole.types import AlignType, ColumnsType, FrameGroupItem, LayoutType
from styledconsole.utils.terminal import TerminalProfile

if TYPE_CHECKING:
    from styledconsole.builders import (
        BannerBuilder,
        FrameBuilder,
        LayoutBuilder,
        TableBuilder,
    )
    from styledconsole.core.group import FrameGroupContext
    from styledconsole.export import ImageTheme
    from styledconsole.model import ConsoleObject
    from styledconsole.rendering import RenderContext


class Console:
    """High-level console rendering facade with Rich backend.

    The Console class is the main entry point for StyledConsole, providing
    a unified API for rendering frames, banners, styled text, and more.
    It integrates with Rich for ANSI rendering and supports HTML export
    via recording mode.

    Phase 4.4: Refactored to delegate to specialized managers:
        - TerminalManager: Terminal detection and capabilities
        - RenderingEngine: Frame, banner, text, rule, newline rendering
        - ExportManager: HTML and text export functionality

    Features:
        - Terminal capability detection
        - Frame and banner rendering
        - Styled text output with colors and formatting
        - Recording mode for HTML export
        - Debug logging support
        - Custom output streams

    Example:
        >>> console = Console()
        >>> console.frame("Hello World", title="Greeting", border="solid")
        >>> console.banner("SUCCESS", font="slant", start_color="green")
        >>> console.text("Status: OK", color="green", bold=True)

    Attributes:
        terminal_profile: Detected terminal capabilities (if detection enabled)
    """

    def __init__(
        self,
        *,
        detect_terminal: bool = True,
        record: bool = False,
        width: int | None = None,
        file: TextIO | None = None,
        debug: bool = False,
        theme: Theme | str | None = None,
        policy: RenderPolicy | None = None,
    ):
        """Initialize Console with optional terminal detection and recording.

        Args:
            detect_terminal: Automatically detect terminal capabilities (color depth,
                emoji support, dimensions). Defaults to True.
            record: Enable recording mode for HTML export. When True, all output is
                captured for later export via export_html(). Defaults to False.
            width: Fixed console width in characters. If None, auto-detected from
                terminal or uses Rich default (80). Defaults to None.
            file: Output stream for console output. Defaults to sys.stdout.
            debug: Enable debug logging for library internals. Useful for
                troubleshooting rendering issues. Defaults to False.
            theme: Color theme for consistent styling. Can be a Theme instance,
                a theme name string ("dark", "monokai", etc.), or None for default.
                Defaults to None.
            policy: Rendering policy for environment-aware output. Controls unicode,
                color, and emoji rendering. If None, auto-detects from environment
                (respects NO_COLOR, CI, TERM=dumb, etc.). Defaults to None.

        Example:
            >>> # Basic usage
            >>> console = Console()

            >>> # Recording mode for HTML export
            >>> console = Console(record=True)
            >>> console.text("Test")
            >>> html = console.export_html()

            >>> # Custom width and output stream
            >>> import io
            >>> buffer = io.StringIO()
            >>> console = Console(width=100, file=buffer)

            >>> # With theme
            >>> from styledconsole import THEMES
            >>> console = Console(theme=THEMES.MONOKAI)

            >>> # Debug mode
            >>> console = Console(debug=True)

            >>> # With explicit policy
            >>> from styledconsole import RenderPolicy
            >>> console = Console(policy=RenderPolicy.ci_friendly())
        """
        # Resolve policy (auto-detect from environment if not provided)
        self._policy = policy if policy is not None else get_default_policy()

        # Apply policy to global icon system
        self._policy.apply_to_icons()

        # Apply render target to global width calculation system
        # This ensures visual_width() uses correct calculations for image/html export
        from styledconsole.utils.text import set_render_target

        set_render_target(self._policy.render_target)

        # Initialize terminal manager (handles detection and color system)
        self._terminal = TerminalManager(detect=detect_terminal, debug=debug)

        # Enable virtual terminal mode for exports
        # This ensures exporters get consistent "perfect terminal" behavior
        if self._policy.render_target in ("image", "html"):
            self._terminal.set_virtual_mode(True)
            # Patch rich.cells.cell_len to match visual_width for consistent layout
            # This must happen in __init__ before any rendering, not at export time,
            # because Rich calculates layout during .frame()/.print() calls.
            # Note: This affects terminal preview output from export consoles, but
            # that's acceptable - it's just preview. Real terminal consoles are unaffected.
            self._patch_rich_cell_len_for_export()

        # Resolve theme
        if isinstance(theme, str):
            self._theme = THEMES.get(theme) or DEFAULT_THEME
        elif isinstance(theme, Theme):
            self._theme = theme
        else:
            self._theme = DEFAULT_THEME

        # Determine color system based on policy
        color_system = self._terminal.get_color_system() if self._policy.color else None

        # Determine if we should force terminal mode
        # Force terminal if: (1) terminal supports ANSI, OR (2) policy explicitly enables color
        # This ensures colors work in non-TTY environments when policy.color=True
        force_terminal = self._terminal.should_force_terminal() or self._policy.color

        # Convert our theme to Rich theme for markup support
        # This enables Rich markup like [success], [error], [primary] to work
        rich_theme = self._theme.to_rich_theme()

        # Initialize Rich console with terminal settings
        self._rich_console = RichConsole(
            record=record,
            width=width,
            file=file or sys.stdout,
            force_terminal=force_terminal,
            color_system=color_system,
            theme=rich_theme,
        )

        # Initialize rendering engine (handles frame, banner, text, rule, newline)
        self._renderer = RenderingEngine(self._rich_console, debug=debug, policy=self._policy)

        # Initialize export manager (handles HTML and text export)
        self._exporter = ExportManager(self._rich_console, debug=debug)

        # Store debug flag for backward compatibility
        self._debug = debug

    # Rich modules that cache cell_len at import time and need patching
    _RICH_MODULES_WITH_CELL_LEN = (
        "rich.cells",
        "rich.text",
        "rich.panel",
        "rich.containers",
        "rich.rule",
        "rich.syntax",
        "rich.pretty",
        "rich._wrap",
        "rich.segment",
    )

    def _patch_rich_cell_len_for_export(self) -> None:
        """Patch rich.cells.cell_len to use visual_width for export mode.

        This ensures Rich's internal layout (tables/panels) uses the same
        emoji widths as our visual_width function, preventing drift in exports.

        Rich modules import cell_len at module load time, caching the function
        reference. We must patch BOTH the source (rich.cells) AND all modules
        that have cached the reference, otherwise they continue using the
        original function.

        Additionally, Rich uses LRU-cached functions (cached_cell_len,
        get_character_cell_size) that must be cleared and patched to prevent
        stale cached values from causing misalignment.

        Note: This is a TEMPORARY patch that gets restored when Console is destroyed
        or when _restore_rich_cell_len() is called.
        """
        import sys

        from styledconsole.utils.text import visual_width

        try:
            from rich import cells as rich_cells

            # Backup originals ONCE per Console instance
            if not hasattr(self, "_original_cell_len"):
                self._original_cell_len = rich_cells.cell_len  # type: ignore[attr-defined]
            if not hasattr(self, "_original_cached_cell_len"):
                self._original_cached_cell_len = rich_cells.cached_cell_len  # type: ignore[attr-defined]

            def _export_cell_len(text: str) -> int:
                """Use visual_width which respects render target context."""
                return visual_width(text)

            # Clear Rich's LRU caches to prevent stale cached values
            # These caches may contain pre-patch width calculations
            if hasattr(rich_cells.cached_cell_len, "cache_clear"):
                rich_cells.cached_cell_len.cache_clear()  # type: ignore[attr-defined]
            if hasattr(rich_cells.get_character_cell_size, "cache_clear"):
                rich_cells.get_character_cell_size.cache_clear()  # type: ignore[attr-defined]

            # Apply the patch to rich.cells (the source)
            rich_cells.cell_len = _export_cell_len  # type: ignore[assignment,attr-defined]
            rich_cells.cached_cell_len = _export_cell_len  # type: ignore[assignment,attr-defined]

            # Also patch all Rich modules that have cached cell_len at import time
            # This is critical because `from .cells import cell_len` creates a
            # local binding that doesn't update when we patch rich.cells.cell_len
            for module_name in self._RICH_MODULES_WITH_CELL_LEN:
                if module_name in sys.modules:
                    module = sys.modules[module_name]
                    if hasattr(module, "cell_len"):
                        module.cell_len = _export_cell_len  # type: ignore[assignment,attr-defined]
                    if hasattr(module, "cached_cell_len"):
                        module.cached_cell_len = _export_cell_len  # type: ignore[assignment,attr-defined]

            self._cell_len_patched = True
        except ImportError:
            self._cell_len_patched = False

    def _restore_rich_cell_len(self) -> None:
        """Restore original rich.cells.cell_len after export."""
        import sys

        if not hasattr(self, "_cell_len_patched") or not self._cell_len_patched:
            return

        try:
            from rich import cells as rich_cells

            if hasattr(self, "_original_cell_len"):
                original_cell_len = self._original_cell_len
                original_cached = getattr(self, "_original_cached_cell_len", original_cell_len)

                # Restore in rich.cells (the source)
                rich_cells.cell_len = original_cell_len  # type: ignore[assignment,attr-defined]
                rich_cells.cached_cell_len = original_cached  # type: ignore[assignment,attr-defined]

                # Restore in all Rich modules that we patched
                for module_name in self._RICH_MODULES_WITH_CELL_LEN:
                    if module_name in sys.modules:
                        module = sys.modules[module_name]
                        if hasattr(module, "cell_len"):
                            module.cell_len = original_cell_len  # type: ignore[assignment,attr-defined]
                        if hasattr(module, "cached_cell_len"):
                            module.cached_cell_len = original_cached  # type: ignore[assignment,attr-defined]

                self._cell_len_patched = False
        except ImportError:
            pass

    @property
    def theme(self) -> Theme:
        """Get the current theme.

        Returns:
            The active Theme instance.
        """
        return self._theme

    @property
    def policy(self) -> RenderPolicy:
        """Get the current rendering policy.

        Returns:
            The active RenderPolicy instance.

        Example:
            >>> console = Console()
            >>> if console.policy.emoji:
            ...     print("Emoji enabled")
            >>> print(f"Icon mode: {console.policy.icon_mode}")
        """
        return self._policy

    @property
    def terminal_profile(self) -> TerminalProfile | None:
        """Get detected terminal capabilities.

        Returns:
            TerminalProfile with capabilities (ANSI support, color depth, emoji safety,
            dimensions) if terminal detection was enabled, None otherwise.

        Example:
            >>> console = Console(detect_terminal=True)
            >>> if console.terminal_profile and console.terminal_profile.emoji_safe:
            ...     print("Emoji supported: 🚀")
        """
        return self._terminal.profile

    def render_frame(
        self,
        content: str | list[str],
        *,
        title: str | None = None,
        border: str = "solid",
        width: int | None = None,
        padding: int = 1,
        align: AlignType = "left",
        frame_align: AlignType | None = None,
        margin: int | tuple[int, int, int, int] = 0,
        content_color: str | None = None,
        border_color: str | None = None,
        title_color: str | None = None,
        # Effect system (v0.9.9.3+)
        effect: EffectSpec | str | None = None,
        # Legacy gradient params (deprecated, use effect= instead)
        start_color: str | None = None,
        end_color: str | None = None,
        border_gradient_start: str | None = None,
        border_gradient_end: str | None = None,
        border_gradient_direction: str = "vertical",
    ) -> str:
        """Render a framed content box to a string.

        Similar to frame(), but returns the rendered string instead of printing it.
        Useful for nested frames or capturing output.

        Args:
            See frame() for argument details.

        Returns:
            Rendered frame as a string containing ANSI escape codes.
        """
        # Resolve effect from new or legacy parameters
        resolved_effect = self._resolve_effect(
            effect=effect,
            start_color=start_color,
            end_color=end_color,
            border_gradient_start=border_gradient_start,
            border_gradient_end=border_gradient_end,
            border_gradient_direction=border_gradient_direction,
        )

        # Resolve style using helper
        resolved_context = self._resolve_frame_style(
            style=None,  # render_frame doesn't support style= parameter
            title=title,
            border=border,
            width=width,
            padding=padding,
            align=align,
            frame_align=frame_align,
            margin=margin,
            content_color=content_color,
            border_color=border_color,
            title_color=title_color,
            start_color=start_color,
            end_color=end_color,
            border_gradient_start=border_gradient_start,
            border_gradient_end=border_gradient_end,
            border_gradient_direction=border_gradient_direction,
            effect=resolved_effect,
        )

        return self._renderer.render_frame_to_string(content, context=resolved_context)

    def _normalize_theme_color(self, color: str | None) -> str | None:
        """Resolve semantic color and normalize for Rich.

        Combines theme.resolve_color() with normalize_color_for_rich() to
        convert semantic names (like "success") to Rich-compatible colors.

        Args:
            color: Semantic color name or literal color value.

        Returns:
            Normalized color string ready for Rich, or None.
        """
        if color is None:
            return None
        from styledconsole.utils.color import normalize_color_for_rich

        return normalize_color_for_rich(self._theme.resolve_color(color))

    def _resolve_color(
        self,
        arg_val: str | None,
        style_val: str | None,
    ) -> str | None:
        """Resolve a color with precedence: arg > style > None."""
        if arg_val is not None:
            return self._normalize_theme_color(arg_val)
        if style_val is not None:
            return self._normalize_theme_color(style_val)
        return None

    def _resolve_gradient_colors(
        self,
        arg_start: str | None,
        arg_end: str | None,
        style_start: str | None,
        style_end: str | None,
        theme_gradient: Any,
    ) -> tuple[str | None, str | None]:
        """Resolve gradient colors with precedence: arg > style > theme."""
        final_start = arg_start if arg_start is not None else style_start
        final_end = arg_end if arg_end is not None else style_end

        if final_start is None and theme_gradient is not None:
            final_start = theme_gradient.start
            final_end = theme_gradient.end

        return (
            self._normalize_theme_color(final_start),
            self._normalize_theme_color(final_end),
        )

    def _resolve_effect(
        self,
        effect: EffectSpec | str | None,
        start_color: str | None,
        end_color: str | None,
        border_gradient_start: str | None,
        border_gradient_end: str | None,
        border_gradient_direction: str,
    ) -> EffectSpec | None:
        """Resolve effect parameter, handling backward compatibility.

        Args:
            effect: New effect parameter (EffectSpec, preset name, or None).
            start_color: Legacy content gradient start color.
            end_color: Legacy content gradient end color.
            border_gradient_start: Legacy border gradient start color.
            border_gradient_end: Legacy border gradient end color.
            border_gradient_direction: Legacy border gradient direction.

        Returns:
            Resolved EffectSpec or None.

        Note:
            When legacy gradient parameters are used, a deprecation warning
            is emitted. The effect= parameter takes precedence.
        """
        # If explicit effect provided, use it
        if effect is not None:
            if isinstance(effect, str):
                # EFFECTS.get() raises KeyError with helpful message if not found
                return EFFECTS.get(effect)
            return effect

        # Backward compat: convert old content gradient params to effect
        if start_color is not None and end_color is not None:
            warnings.warn(
                "start_color/end_color are deprecated. "
                "Use effect=EffectSpec.gradient(start, end) instead.",
                DeprecationWarning,
                stacklevel=4,
            )
            return EffectSpec.gradient(
                start_color,
                end_color,
                target="content",
            )

        # Backward compat: convert old border gradient params to effect
        if border_gradient_start is not None and border_gradient_end is not None:
            warnings.warn(
                "border_gradient_start/end are deprecated. "
                "Use effect=EffectSpec.gradient(..., target='border') instead.",
                DeprecationWarning,
                stacklevel=4,
            )
            direction = border_gradient_direction
            if direction not in ("vertical", "horizontal", "diagonal"):
                direction = "vertical"
            return EffectSpec.gradient(
                border_gradient_start,
                border_gradient_end,
                direction=direction,  # type: ignore[arg-type]
                target="border",
            )

        return None

    def _resolve_simple_attrs(
        self,
        style: StyleContext | None,
        title: str | None,
        border: str | None,
        width: int | None,
        padding: int | None,
        align: AlignType | None,
        frame_align: AlignType | None,
        margin: int | tuple[int, int, int, int] | None,
        border_gradient_direction: str,
    ) -> dict[str, Any]:
        """Resolve simple attributes with arg > style > default precedence."""
        return {
            "border_style": border
            if border is not None
            else (style.border_style if style else "solid"),
            "padding": padding if padding is not None else (style.padding if style else 1),
            "align": align if align is not None else (style.align if style else "left"),
            "frame_align": frame_align
            if frame_align is not None
            else (style.frame_align if style else None),
            "margin": margin if margin is not None else (style.margin if style else 0),
            "width": width if width is not None else (style.width if style else None),
            "title": title if title is not None else (style.title if style else None),
            "border_gradient_direction": (
                border_gradient_direction
                if border_gradient_direction != "vertical"
                else (style.border_gradient_direction if style else "vertical")
            ),
        }

    def _resolve_frame_style(
        self,
        style: StyleContext | None,
        title: str | None,
        border: str | None,
        width: int | None,
        padding: int | None,
        align: AlignType | None,
        frame_align: AlignType | None,
        margin: int | tuple[int, int, int, int] | None,
        content_color: str | None,
        border_color: str | None,
        title_color: str | None,
        start_color: str | None,
        end_color: str | None,
        border_gradient_start: str | None,
        border_gradient_end: str | None,
        border_gradient_direction: str,
        effect: EffectSpec | None = None,
    ) -> StyleContext:
        """Resolve effective style parameters from arguments and style object."""
        # Resolve simple attributes
        attrs = self._resolve_simple_attrs(
            style,
            title,
            border,
            width,
            padding,
            align,
            frame_align,
            margin,
            border_gradient_direction,
        )

        # Resolve colors
        resolved_content_color = self._resolve_color(
            content_color, style.content_color if style else None
        )
        resolved_border_color = self._resolve_color(
            border_color, style.border_color if style else None
        )
        resolved_title_color = self._resolve_color(
            title_color, style.title_color if style else None
        )

        # If effect is provided, it takes precedence over legacy gradient params
        resolved_effect = effect if effect is not None else (style.effect if style else None)

        # Resolve content gradient (legacy, only if no effect)
        resolved_start, resolved_end = None, None
        if resolved_effect is None:
            resolved_start, resolved_end = self._resolve_gradient_colors(
                start_color,
                end_color,
                style.start_color if style else None,
                style.end_color if style else None,
                self._theme.text_gradient,
            )

        # Resolve border gradient (legacy, only if no effect)
        bg_start, bg_end = None, None
        if resolved_effect is None:
            bg_start, bg_end = self._resolve_gradient_colors(
                border_gradient_start,
                border_gradient_end,
                style.border_gradient_start if style else None,
                style.border_gradient_end if style else None,
                self._theme.border_gradient,
            )
        # Override direction from theme if applicable
        eff_bg_dir = attrs["border_gradient_direction"]
        if (
            border_gradient_start is None
            and (style is None or style.border_gradient_start is None)
            and self._theme.border_gradient is not None
            and eff_bg_dir == "vertical"
        ):
            eff_bg_dir = self._theme.border_gradient.direction

        return StyleContext(
            width=attrs["width"],
            padding=attrs["padding"],
            align=attrs["align"],
            frame_align=attrs["frame_align"],
            margin=attrs["margin"],
            border_style=attrs["border_style"],
            border_color=resolved_border_color,
            border_gradient_start=bg_start,
            border_gradient_end=bg_end,
            border_gradient_direction=eff_bg_dir,
            content_color=resolved_content_color,
            start_color=resolved_start,
            end_color=resolved_end,
            effect=resolved_effect,
            title=attrs["title"],
            title_color=resolved_title_color,
        )

    def frame(
        self,
        content: str | list[str],
        style: StyleContext | None = None,
        *,
        title: str | None = None,
        border: str | None = None,
        width: int | None = None,
        padding: int | None = None,
        align: AlignType | None = None,
        frame_align: AlignType | None = None,
        margin: int | tuple[int, int, int, int] | None = None,
        content_color: str | None = None,
        border_color: str | None = None,
        title_color: str | None = None,
        # Effect system (v0.9.9.3+)
        effect: EffectSpec | str | None = None,
        # Legacy gradient params (deprecated, use effect= instead)
        start_color: str | None = None,
        end_color: str | None = None,
        border_gradient_start: str | None = None,
        border_gradient_end: str | None = None,
        border_gradient_direction: str = "vertical",
    ) -> None:
        """Render and print a framed content box.

        This is the primary method for displaying content in a box.

        Args:
            content: The text or list of strings to display inside the frame.
            style: Optional StyleContext object containing styling parameters.
                If provided, it serves as the base configuration.
            title: Optional title to display in the top border.
            border: Border style (\"solid\", \"rounded\", \"double\", etc.).
                Supported: \"heavy\", \"thick\", \"ascii\", \"minimal\".
                Defaults to "solid" if not specified in style.
            width: Explicit width of the frame. If None, fits to content.
            padding: Padding between border and content. Defaults to 1 if not specified in style.
            align: Content alignment within the frame ("left", "center", "right").
                Defaults to "left" if not specified in style.
            frame_align: Alignment of the frame itself on the screen ("left", "center", "right").
            margin: Margin around the frame. Defaults to 0 if not specified in style.
            content_color: Color of the content text.
            border_color: Color of the border.
            title_color: Color of the title text.
            effect: Effect specification for gradients/rainbows. Can be:
                - An EffectSpec instance: EffectSpec.gradient("red", "blue")
                - A preset name: "fire", "ocean", "rainbow", etc.
                - None for no effect (default)
            start_color: DEPRECATED. Use effect=EffectSpec.gradient() instead.
            end_color: DEPRECATED. Use effect=EffectSpec.gradient() instead.
            border_gradient_start: DEPRECATED. Use effect= with target="border" instead.
            border_gradient_end: DEPRECATED. Use effect= with target="border" instead.
            border_gradient_direction: Direction of border gradient ("vertical", "horizontal").

        Example:
            >>> from styledconsole import Console
            >>> from styledconsole.effects import EFFECTS, EffectSpec
            >>> console = Console()
            >>>
            >>> # Using preset name
            >>> console.frame("Hello", effect="fire")
            >>>
            >>> # Using EFFECTS registry
            >>> console.frame("World", effect=EFFECTS.ocean)
            >>>
            >>> # Using custom EffectSpec
            >>> console.frame("Custom", effect=EffectSpec.gradient("red", "blue"))
        """
        # Resolve effect from new or legacy parameters
        resolved_effect = self._resolve_effect(
            effect=effect,
            start_color=start_color,
            end_color=end_color,
            border_gradient_start=border_gradient_start,
            border_gradient_end=border_gradient_end,
            border_gradient_direction=border_gradient_direction,
        )

        # Resolve style using helper
        resolved_context = self._resolve_frame_style(
            style=style,
            title=title,
            border=border,
            width=width,
            padding=padding,
            align=align,
            frame_align=frame_align,
            margin=margin,
            content_color=content_color,
            border_color=border_color,
            title_color=title_color,
            start_color=start_color,
            end_color=end_color,
            border_gradient_start=border_gradient_start,
            border_gradient_end=border_gradient_end,
            border_gradient_direction=border_gradient_direction,
            effect=resolved_effect,
        )

        # Check if we're inside a group context
        from styledconsole.core.group import get_active_group

        active_group = get_active_group()
        if active_group is not None:
            # Capture using resolved values
            active_group.capture_frame(
                content,
                title=resolved_context.title,
                border=resolved_context.border_style,
                width=resolved_context.width,
                padding=resolved_context.padding,
                align=resolved_context.align,
                frame_align=resolved_context.frame_align,
                margin=resolved_context.margin,
                content_color=resolved_context.content_color,
                border_color=resolved_context.border_color,
                title_color=resolved_context.title_color,
                start_color=resolved_context.start_color,
                end_color=resolved_context.end_color,
                border_gradient_start=resolved_context.border_gradient_start,
                border_gradient_end=resolved_context.border_gradient_end,
                border_gradient_direction=resolved_context.border_gradient_direction,
            )
            return

        # Normal print behavior (using context)
        self._renderer.print_frame(content, context=resolved_context)

    def render_frame_group(
        self,
        items: list[FrameGroupItem],
        *,
        title: str | None = None,
        border: str = "rounded",
        width: int | None = None,
        padding: int = 1,
        align: AlignType = "left",
        border_color: str | None = None,
        title_color: str | None = None,
        border_gradient_start: str | None = None,
        border_gradient_end: str | None = None,
        layout: LayoutType = "vertical",
        gap: int = 1,
        inherit_style: bool = False,
        columns: ColumnsType = "auto",
        min_columns: int = 2,
        item_width: int | None = None,
    ) -> str:
        """Render a group of frames to a string.

        Creates multiple frames arranged within an outer container frame.
        Supports vertical, horizontal, and grid layouts.

        Args:
            items: List of frame item dictionaries. Each dict must have 'content'
                key and may optionally include: title, border, border_color,
                content_color, title_color.
            title: Optional title for the outer container frame.
            border: Border style for outer frame. One of: "solid", "rounded",
                "double", "heavy", "thick", "ascii", "minimal", "dashed".
                Defaults to "rounded".
            width: Fixed width for outer frame. If None, auto-calculated.
                Defaults to None.
            padding: Padding (spaces) inside outer frame. Defaults to 1.
            align: Content alignment within outer frame. Defaults to "left".
            border_color: Color for outer frame border. Accepts CSS4 names,
                hex codes, or RGB tuples.
            title_color: Color for outer frame title.
            border_gradient_start: Starting color for outer border gradient.
            border_gradient_end: Ending color for outer border gradient.
            layout: Layout mode for inner frames:
                - "vertical": Stack frames top-to-bottom (default)
                - "horizontal": Place all frames side-by-side in one row
                - "grid": Arrange frames in rows/columns
            gap: Space between frames. For vertical layout, number of blank lines.
                For horizontal/grid, number of characters. Defaults to 1.
            inherit_style: If True, inner frames inherit outer border style
                when not explicitly specified. Defaults to False.
            columns: Number of columns for horizontal/grid layout.
                Use "auto" to calculate from terminal width. Defaults to "auto".
            min_columns: Minimum columns when columns="auto". Defaults to 2.
            item_width: Width of each item frame for horizontal/grid layout.
                If None, uses 35. Defaults to None.

        Returns:
            Rendered frame group as a string containing ANSI escape codes.
            Can be used for nesting within other frames.

        Example:
            >>> console = Console()
            >>> # Vertical layout (default)
            >>> group = console.render_frame_group(
            ...     [{"content": "A"}, {"content": "B"}],
            ...     title="Vertical",
            ... )
            >>> # Grid layout with auto columns
            >>> group = console.render_frame_group(
            ...     [{"content": f"Item {i}"} for i in range(8)],
            ...     layout="grid",
            ...     columns="auto",
            ...     min_columns=2,
            ... )
        """
        return self._renderer.render_frame_group_to_string(
            items,
            title=title,
            border=border,
            width=width,
            padding=padding,
            align=align,
            border_color=border_color,
            title_color=title_color,
            border_gradient_start=border_gradient_start,
            border_gradient_end=border_gradient_end,
            layout=layout,
            gap=gap,
            inherit_style=inherit_style,
            columns=columns,
            min_columns=min_columns,
            item_width=item_width,
        )

    def frame_group(
        self,
        items: list[FrameGroupItem],
        *,
        title: str | None = None,
        border: str = "rounded",
        width: int | None = None,
        padding: int = 1,
        align: AlignType = "left",
        border_color: str | None = None,
        title_color: str | None = None,
        border_gradient_start: str | None = None,
        border_gradient_end: str | None = None,
        layout: LayoutType = "vertical",
        gap: int = 1,
        inherit_style: bool = False,
        margin: int | tuple[int, int, int, int] = 0,
        frame_align: AlignType | None = None,
        columns: ColumnsType = "auto",
        min_columns: int = 2,
        item_width: int | None = None,
    ) -> None:
        """Render and print a group of frames.

        Creates multiple frames arranged within an outer container frame.
        Perfect for dashboards, status panels, multi-section displays, and
        organized information layouts.

        Args:
            items: List of frame item dictionaries. Each dict must have 'content'
                key and may optionally include: title, border, border_color,
                content_color, title_color.
            title: Optional title for the outer container frame.
            border: Border style for outer frame. One of: "solid", "rounded",
                "double", "heavy", "thick", "ascii", "minimal", "dashed".
                Defaults to "rounded".
            width: Fixed width for outer frame. If None, auto-calculated.
                Defaults to None.
            padding: Padding (spaces) inside outer frame. Defaults to 1.
            align: Content alignment within outer frame. Defaults to "left".
            border_color: Color for outer frame border. Accepts CSS4 names,
                hex codes, or RGB tuples.
            title_color: Color for outer frame title.
            border_gradient_start: Starting color for outer border gradient.
            border_gradient_end: Ending color for outer border gradient.
            layout: Layout mode for inner frames:
                - "vertical": Stack frames top-to-bottom (default)
                - "horizontal": Place all frames side-by-side in one row
                - "grid": Arrange frames in rows/columns
            gap: Space between frames. For vertical layout, number of blank lines.
                For horizontal/grid, number of characters. Defaults to 1.
            inherit_style: If True, inner frames inherit outer border style
                when not explicitly specified. Defaults to False.
            margin: Margin around the outer frame.
            frame_align: Alignment of the outer frame on screen.
            columns: Number of columns for horizontal/grid layout.
                Use "auto" to calculate from terminal width. Defaults to "auto".
            min_columns: Minimum columns when columns="auto". Defaults to 2.
            item_width: Width of each item frame for horizontal/grid layout.
                If None, uses 35. Defaults to None.

        Example:
            >>> console = Console()
            >>> # Simple vertical frame group
            >>> console.frame_group(
            ...     [
            ...         {"content": "Status: OK", "title": "System"},
            ...         {"content": "Memory: 4GB", "title": "Resources"},
            ...     ],
            ...     title="Dashboard",
            ...     border="double",
            ... )

            >>> # Grid layout with auto columns
            >>> console.frame_group(
            ...     [{"content": f"Item {i}", "border": "solid"} for i in range(8)],
            ...     layout="grid",
            ...     columns="auto",
            ...     min_columns=2,
            ...     item_width=30,
            ... )

            >>> # Horizontal layout (all in one row)
            >>> console.frame_group(
            ...     [{"content": "A"}, {"content": "B"}, {"content": "C"}],
            ...     layout="horizontal",
            ...     gap=2,
            ... )
        """
        self._renderer.print_frame_group(
            items,
            title=title,
            border=border,
            width=width,
            padding=padding,
            align=align,
            border_color=border_color,
            title_color=title_color,
            border_gradient_start=border_gradient_start,
            border_gradient_end=border_gradient_end,
            layout=layout,
            gap=gap,
            inherit_style=inherit_style,
            margin=margin,
            frame_align=frame_align,
            columns=columns,
            min_columns=min_columns,
            item_width=item_width,
        )

    def group(
        self,
        *,
        title: str | None = None,
        border: str = "rounded",
        border_color: str | None = None,
        title_color: str | None = None,
        border_gradient_start: str | None = None,
        border_gradient_end: str | None = None,
        padding: int = 1,
        width: int | None = None,
        align: AlignType = "left",
        gap: int = 1,
        inherit_style: bool = False,
        align_widths: bool = False,
        margin: int | tuple[int, int, int, int] = 0,
        frame_align: AlignType | None = None,
    ) -> FrameGroupContext:
        """Create a context manager for grouping frames.

        When used as a context manager, any calls to frame() within the block
        are captured and rendered together as a single group when the block exits.

        Args:
            title: Optional title for the outer frame.
            border: Border style for the outer frame.
            border_color: Color for the outer frame border.
            title_color: Color for the outer frame title.
            border_gradient_start: Gradient start for outer border.
            border_gradient_end: Gradient end for outer border.
            padding: Padding inside outer frame. Defaults to 1.
            width: Fixed width for outer frame. Defaults to None (auto).
            align: Content alignment within outer frame.
            gap: Lines between captured frames. Defaults to 1.
            >>> # Aligned widths for status-style layouts
            >>> with console.group(align_widths=True) as group:
            ...     console.frame("Short", title="A")
            ...     console.frame("Much longer content here", title="B")
        """
        from styledconsole.core.group import FrameGroupContext

        return FrameGroupContext(
            console=self,
            title=title,
            border=border,
            border_color=border_color,
            title_color=title_color,
            border_gradient_start=border_gradient_start,
            border_gradient_end=border_gradient_end,
            padding=padding,
            width=width,
            align=align,
            gap=gap,
            inherit_style=inherit_style,
            align_widths=align_widths,
            margin=margin,
            frame_align=frame_align,
        )

    def _print_ansi_output(self, output: str, align: str = "left") -> None:
        """Print ANSI output with proper alignment handling.

        Internal method used by FrameGroupContext to print rendered output.

        Args:
            output: String containing ANSI escape codes.
            align: Alignment for the output ("left", "center", "right").
        """
        from styledconsole.utils.text import create_rich_text

        self._renderer._print_aligned(create_rich_text(output), align)

    def banner(
        self,
        text: str,
        *,
        font: str = "standard",
        # Effect system (v0.9.9.3+)
        effect: EffectSpec | str | None = None,
        # Legacy gradient params (deprecated, use effect= instead)
        start_color: str | None = None,
        end_color: str | None = None,
        rainbow: bool = False,
        border: str | None = None,
        width: int | None = None,
        align: AlignType = "center",
        padding: int = 1,
    ) -> None:
        """Render and print an ASCII art banner.

        Creates large ASCII art text using pyfiglet with optional gradient
        coloring and frame borders. Perfect for headers, titles, and status
        messages.

        Args:
            text: Text to render as ASCII art banner. Emoji characters will
                fallback to plain text rendering.
            font: Pyfiglet font name. Common options: "slant", "banner", "big",
                "digital", "standard". Use BannerRenderer.list_fonts() to see
                all available fonts. Defaults to "standard".
            effect: Effect specification for gradients/rainbows. Can be:
                - An EffectSpec instance: EffectSpec.gradient("red", "blue")
                - A preset name: "fire", "ocean", "rainbow", etc.
                - None for no effect (default)
            start_color: DEPRECATED. Use effect=EffectSpec.gradient() instead.
            end_color: DEPRECATED. Use effect=EffectSpec.gradient() instead.
            rainbow: DEPRECATED. Use effect="rainbow" instead.
            border: Optional border style to frame the banner. One of: "solid",
                "double", "rounded", etc. Defaults to None (no border).
            width: Banner width in characters. If None, auto-calculated.
                Defaults to None.
            align: Banner alignment. One of: "left", "center", "right".
                Defaults to "center". Note: This aligns the ASCII art relative to the
                screen or specified width.
            padding: Horizontal padding when border is used. Defaults to 1.

        Example:
            >>> console = Console()
            >>> console.banner("SUCCESS", font="slant")

            >>> # With effect preset
            >>> console.banner("FIRE", effect="fire")
            >>> console.banner("RAINBOW", effect="rainbow_neon")

            >>> # With custom effect
            >>> console.banner(
            ...     "DEMO",
            ...     font="banner",
            ...     effect=EffectSpec.gradient("red", "blue")
            ... )

            >>> # Legacy (deprecated but still works):
            >>> console.banner("DEMO", start_color="red", end_color="blue")
            >>> console.banner("RAINBOW", rainbow=True)  # Use effect="rainbow" instead
        """
        # Resolve effect parameter
        resolved_effect: EffectSpec | None = None
        effective_rainbow = rainbow
        effective_start = start_color
        effective_end = end_color

        if effect is not None:
            # New effect= parameter takes precedence
            # EFFECTS.get() raises KeyError with helpful message if not found
            resolved_effect = EFFECTS.get(effect) if isinstance(effect, str) else effect

            # Convert effect to banner parameters
            if resolved_effect.is_rainbow():
                effective_rainbow = True
                effective_start = None
                effective_end = None
            elif resolved_effect.is_gradient() or resolved_effect.is_multi_stop():
                effective_rainbow = False
                effective_start = resolved_effect.get_start_color()
                effective_end = resolved_effect.get_end_color()
        else:
            # Legacy parameter handling
            if rainbow:
                warnings.warn(
                    "rainbow=True is deprecated. Use effect='rainbow' instead.",
                    DeprecationWarning,
                    stacklevel=2,
                )
            elif start_color is not None and end_color is not None:
                warnings.warn(
                    "start_color/end_color are deprecated. "
                    "Use effect=EffectSpec.gradient(start, end) instead.",
                    DeprecationWarning,
                    stacklevel=2,
                )

        # Apply theme banner gradient if no explicit gradient provided
        if (
            effective_start is None
            and not effective_rainbow
            and self._theme.banner_gradient is not None
        ):
            effective_start = self._theme.banner_gradient.start
            effective_end = self._theme.banner_gradient.end

        resolved_start_color = self._normalize_theme_color(effective_start)
        resolved_end_color = self._normalize_theme_color(effective_end)

        self._renderer.print_banner(
            text,
            font=font,
            start_color=resolved_start_color,
            end_color=resolved_end_color,
            rainbow=effective_rainbow,
            border=border,
            width=width,
            align=align,
            padding=padding,
        )

    def text(
        self,
        text: str,
        *,
        color: str | None = None,
        bold: bool = False,
        italic: bool = False,
        underline: bool = False,
        dim: bool = False,
        end: str = "\n",
    ) -> None:
        """Print styled text with colors and formatting.

        Simple wrapper around Rich's print functionality for styled text output
        with optional color and text formatting attributes.

        Args:
            text: Text content to print.
            color: Text color. Accepts CSS4 color names ("red", "dodgerblue"),
                or semantic theme colors ("success", "warning", "error", "info",
                "primary", "secondary"). Defaults to None (terminal default).
            bold: Apply bold formatting. Defaults to False.
            italic: Apply italic formatting. Defaults to False.
            underline: Apply underline formatting. Defaults to False.
            dim: Apply dim/faint formatting. Defaults to False.
            end: String appended after text. Defaults to "\\n" (newline).

        Note:
            To align text (e.g. center it), wrap it in a frame or use a layout component.

        Example:
            >>> console = Console()
            >>> console.text("Success!", color="green", bold=True)
            >>> console.text("Warning", color="yellow", italic=True)
            >>> console.text("Error: File not found", color="red", bold=True)

            >>> # Using semantic theme colors
            >>> console = Console(theme="dark")
            >>> console.text("OK", color="success")  # Uses theme.success color
            >>> console.text("Oops", color="error")  # Uses theme.error color

            >>> # No newline
            >>> console.text("Loading", end="")
            >>> console.text("... done!", color="green")
        """
        normalized_color = self._normalize_theme_color(color)

        # Build style string
        styles = []
        if bold:
            styles.append("bold")
        if italic:
            styles.append("italic")
        if underline:
            styles.append("underline")
        if dim:
            styles.append("dim")
        if normalized_color:
            styles.append(normalized_color)

        # Use Rich console directly for dim support
        if styles:
            from rich.text import Text as RichText

            style_str = " ".join(styles)
            rich_text = RichText(text, style=style_str)
            self._rich_console.print(rich_text, end=end, highlight=False)
        else:
            self._renderer.print_text(
                text,
                color=normalized_color,
                bold=bold,
                italic=italic,
                underline=underline,
                end=end,
            )

    def rule(
        self,
        title: str | None = None,
        *,
        color: str = "white",
        style: str = "solid",
        align: AlignType = "center",
    ) -> None:
        """Print a horizontal rule line with optional title.

        Renders a full-width horizontal line (separator) with an optional
        centered title. Useful for section dividers.

        Args:
            title: Optional title text displayed in the center of the rule.
                Defaults to None (plain line).
            color: Rule color. Accepts CSS4 color names or semantic theme
                colors ("primary", "success", etc.). Defaults to "white".
            style: Rule line style. Currently only "solid" is supported
                (Rich limitation). Defaults to "solid".
            align: Title alignment within rule. One of: "left", "center", "right".
                Defaults to "center".

        Example:
            >>> console = Console()
            >>> console.rule()  # Plain line
            >>> console.rule("Section 1", color="blue")
            >>> console.rule("Configuration", color="cyan", align="left")

            >>> # With semantic theme color
            >>> console = Console(theme="dark")
            >>> console.rule("Status", color="primary")
        """
        resolved_color = self._normalize_theme_color(color) or "white"

        self._renderer.print_rule(title=title, color=resolved_color, style=style, align=align)

    def newline(self, count: int = 1) -> None:
        """Print one or more blank lines.

        Simple utility for adding vertical spacing in console output.

        Args:
            count: Number of blank lines to print. Must be >= 0. Defaults to 1.

        Example:
            >>> console = Console()
            >>> console.text("Line 1")
            >>> console.newline()
            >>> console.text("Line 2")
            >>> console.newline(3)  # Three blank lines
            >>> console.text("Line 3")
        """
        self._renderer.print_newline(count=count)

    def clear(self) -> None:
        """Clear the console screen.

        Clears the terminal screen if ANSI support is available. Does nothing
        if terminal doesn't support ANSI escape codes.

        Example:
            >>> console = Console()
            >>> console.text("Some content")
            >>> console.clear()  # Screen is cleared
        """
        profile = self.terminal_profile
        if profile and profile.ansi_support:
            self._rich_console.clear()

    def export_html(self, *, inline_styles: bool = True) -> str:
        """Export recorded console output as HTML.

        Converts all recorded ANSI output to HTML with preserved formatting,
        colors, and styles. Requires recording mode to be enabled during
        Console initialization (record=True).

        Args:
            inline_styles: Use inline CSS styles (True) or CSS classes (False).
                Inline styles are recommended for standalone HTML files or
                email embedding. Defaults to True.

        Returns:
            HTML string with ANSI formatting converted to styled spans.

        Raises:
            RuntimeError: If recording mode was not enabled during initialization.

        Example:
            >>> console = Console(record=True)
            >>> console.frame("Test", title="Demo")
            >>> console.text("Hello", color="green")
            >>> html = console.export_html()
            >>> with open("output.html", "w") as f:
            ...     f.write(html)
        """
        return self._exporter.export_html(inline_styles=inline_styles)

    def export_text(self) -> str:
        """Export recorded console output as plain text.

        Returns all recorded output with ANSI escape codes stripped.
        Useful for logging, testing, or text-only output formats.
        Requires recording mode to be enabled (record=True).

        Returns:
            Plain text string with all ANSI codes removed.

        Raises:
            RuntimeError: If recording mode was not enabled during initialization.

        Example:
            >>> console = Console(record=True)
            >>> console.frame("Test", title="Demo")
            >>> text = console.export_text()
            >>> print(repr(text))  # No ANSI codes
        """
        return self._exporter.export_text()

    def export_png(self, path: str, *, scale: float = 1.0) -> None:
        """Export recorded console output as PNG image.

        Renders all recorded output to a PNG image file, preserving colors
        and styling. Requires Pillow to be installed.

        Args:
            path: Output file path for the PNG image.
            scale: Scale factor for the image (e.g., 2.0 for retina displays).
                Defaults to 1.0.

        Raises:
            RuntimeError: If recording mode was not enabled during initialization.
            ImportError: If Pillow is not installed.

        Example:
            >>> console = Console(record=True)
            >>> console.frame("Hello World", border="rounded")
            >>> console.export_png("output.png")
            >>> console.export_png("output@2x.png", scale=2.0)  # Retina

        Note:
            Requires: pip install styledconsole[image]
        """
        self._exporter._validate_recording_enabled()
        from styledconsole.export import get_image_exporter

        try:
            image_exporter_cls = get_image_exporter()
            exporter = image_exporter_cls(self._rich_console)
            exporter.save_png(path, scale=scale)
        finally:
            # Restore cell_len after export so subsequent terminal output is correct
            self._restore_rich_cell_len()

    def export_webp(
        self,
        path: str,
        *,
        quality: int = 90,
        animated: bool = False,
        fps: int = 10,
        loop: int = 0,
        theme: ImageTheme | None = None,
        auto_crop: bool = False,
        crop_margin: int = 20,
    ) -> None:
        """Export recorded console output as WebP image.

        Renders output to WebP format, which offers better compression than PNG.
        Supports both static and animated output. Requires Pillow.

        Args:
            path: Output file path for the WebP image.
            quality: Image quality (0-100). Higher is better. Defaults to 90.
            animated: If True, exports as animated WebP using captured frames.
                Defaults to False.
            fps: Frames per second for animation. Defaults to 10.
            loop: Number of animation loops (0 = infinite). Defaults to 0.
            theme: Image theme with colors, font size, and optional fixed terminal size.
                Use ImageTheme(terminal_size=(80, 24)) for consistent sizing.
            auto_crop: If True, automatically crop to content with margin.
            crop_margin: Margin in pixels when auto_crop is True. Defaults to 20.

        Raises:
            RuntimeError: If recording mode was not enabled during initialization.
            ImportError: If Pillow is not installed.

        Example:
            >>> console = Console(record=True)
            >>> console.frame("Hello World", border="rounded")
            >>> console.export_webp("output.webp")
            >>> console.export_webp("output.webp", quality=95)  # Higher quality
            >>> # Fixed terminal size for consistent image dimensions:
            >>> from styledconsole.export import ImageTheme
            >>> theme = ImageTheme(terminal_size=(80, 24))
            >>> console.export_webp("output.webp", theme=theme)
            >>> # Auto-crop to content:
            >>> console.export_webp("output.webp", theme=theme, auto_crop=True)

        Note:
            Requires: pip install styledconsole[image]
        """
        self._exporter._validate_recording_enabled()
        from styledconsole.export import get_image_exporter

        # Patch cell_len only during export to avoid affecting terminal output
        self._patch_rich_cell_len_for_export()
        try:
            image_exporter_cls = get_image_exporter()
            exporter = image_exporter_cls(self._rich_console, theme=theme)
            exporter.save_webp(
                path,
                quality=quality,
                animated=animated,
                fps=fps,
                loop=loop,
                do_auto_crop=auto_crop,
                crop_margin=crop_margin,
            )
        finally:
            # Restore cell_len after export so subsequent terminal output is correct
            self._restore_rich_cell_len()

    def export_gif(self, path: str, *, fps: int = 10, loop: int = 0) -> None:
        """Export recorded console output as animated GIF.

        Renders output as GIF image. For animations, use capture_frame() to
        record multiple states, then export_gif() to save. Requires Pillow.

        Args:
            path: Output file path for the GIF image.
            fps: Frames per second for animation. Defaults to 10.
            loop: Number of animation loops (0 = infinite). Defaults to 0.

        Raises:
            RuntimeError: If recording mode was not enabled during initialization.
            ImportError: If Pillow is not installed.

        Example:
            >>> console = Console(record=True)
            >>> console.frame("Hello World", border="rounded")
            >>> console.export_gif("output.gif")

        Note:
            Requires: pip install styledconsole[image]
        """
        self._exporter._validate_recording_enabled()
        from styledconsole.export import get_image_exporter

        try:
            image_exporter_cls = get_image_exporter()
            exporter = image_exporter_cls(self._rich_console)
            exporter.save_gif(path, fps=fps, loop=loop)
        finally:
            # Restore cell_len after export so subsequent terminal output is correct
            self._restore_rich_cell_len()

    def print(self, *args: Any, **kwargs: Any) -> None:
        """Direct pass-through to Rich console print.

        Provides direct access to Rich's print method for advanced use cases
        not covered by Console's high-level methods.

        Args:
            *args: Positional arguments passed to Rich console.print()
            **kwargs: Keyword arguments passed to Rich console.print()

        Example:
            >>> console = Console()
            >>> # Use Rich markup directly
            >>> console.print("[bold red]Error:[/bold red] Something failed")
            >>> # Rich Table, Panel, etc.
            >>> from rich.table import Table
            >>> table = Table()
            >>> console.print(table)
        """
        self._rich_console.print(*args, **kwargs)

    def progress(
        self,
        *,
        transient: bool = False,
        auto_refresh: bool = True,
        expand: bool = False,
    ) -> StyledProgress:
        """Create a styled progress bar context manager.

        Returns a StyledProgress instance that integrates with the console's
        theme for consistent styling. Use as a context manager to track
        progress of long-running operations.

        Args:
            transient: If True, progress bar disappears after completion.
                Useful for temporary progress indicators. Defaults to False.
            auto_refresh: If True, automatically refresh the display.
                Defaults to True.
            expand: If True, progress bar expands to full width.
                Defaults to False.

        Returns:
            StyledProgress context manager for tracking progress.

        Example:
            >>> console = Console()
            >>> with console.progress() as progress:
            ...     task = progress.add_task("Processing...", total=100)
            ...     for i in range(100):
            ...         # do work
            ...         progress.update(task, advance=1)

            >>> # With transient progress (disappears when done)
            >>> with console.progress(transient=True) as progress:
            ...     task = progress.add_task("Downloading...", total=1000)
            ...     # ...
        """
        return StyledProgress(
            theme=self._theme,
            console=self._rich_console,
            transient=transient,
            auto_refresh=auto_refresh,
            expand=expand,
            policy=self._policy,
        )

    def resolve_color(self, color: str | None) -> str | None:
        """Resolve a semantic color name using the current theme.

        If the color is a semantic name (like 'success', 'error', 'primary'),
        returns the theme's color for that semantic. Otherwise returns the
        color unchanged.

        Args:
            color: A semantic color name or literal color value.

        Returns:
            The resolved color value.

        Example:
            >>> console = Console(theme=THEMES.DARK)
            >>> console.resolve_color("success")  # Returns "lime"
            >>> console.resolve_color("red")      # Returns "red" (unchanged)
        """
        return self._theme.resolve_color(color)

    def columns(
        self,
        renderables: Iterable[Any],
        padding: int | tuple[int] | tuple[int, int] | tuple[int, int, int, int] = (0, 2),
        *,
        width: int | None = None,
        expand: bool = False,
        equal: bool = False,
        column_first: bool = False,
        right_to_left: bool = False,
        align: AlignType | None = None,
        title: str | None = None,
    ) -> None:
        """Display renderables in columns with automatic policy awareness.

        Creates a multi-column layout with automatic emoji sanitization
        and VS16 emoji width fix for proper alignment.

        Args:
            renderables: Iterable of renderable items (strings, Rich objects, etc.).
            padding: Padding around each column. Can be int or tuple
                (top, right, bottom, left). Defaults to (0, 2).
            width: Width constraint for the entire column layout.
            expand: Expand columns to fill available width. Defaults to False.
            equal: Make all columns equal width. Defaults to False.
            column_first: Fill columns vertically instead of horizontally.
                Defaults to False.
            right_to_left: Render columns from right to left. Defaults to False.
            align: Alignment of content within columns ("left", "center", "right").
            title: Optional title for the columns layout.

        Example:
            >>> console = Console()
            >>> # Simple columns
            >>> console.columns(["Item 1", "Item 2", "Item 3"])

            >>> # With custom padding and equal widths
            >>> console.columns(
            ...     ["Short", "Medium Text", "Very Long Item"],
            ...     padding=(0, 3),
            ...     equal=True,
            ... )

            >>> # Vertical filling (column-first)
            >>> items = [f"Item {i}" for i in range(10)]
            >>> console.columns(items, column_first=True)

            >>> # With emoji (automatically sanitized based on policy)
            >>> console.columns(["✅ Done", "⚠️ Warning", "❌ Error"])
        """
        from styledconsole.columns import StyledColumns

        columns_obj = StyledColumns(
            renderables,
            padding=padding,
            policy=self._policy,
            width=width,
            expand=expand,
            equal=equal,
            column_first=column_first,
            right_to_left=right_to_left,
            align=align,
            title=title,
        )
        self._rich_console.print(columns_obj)

    # =========================================================================
    # Builder Factory Methods (Phase 5 - v0.10.0 API)
    # =========================================================================

    def build_frame(self) -> FrameBuilder:
        """Create a FrameBuilder for fluent frame construction.

        Returns a builder that can be configured with method chaining,
        then rendered with .render() or converted to object with .build().

        Returns:
            FrameBuilder instance bound to this console.

        Example:
            >>> console = Console()
            >>> # Fluent building and rendering
            >>> console.build_frame().content("Hello").title("Greeting").effect("ocean").render()
            >>>
            >>> # Build object for later use
            >>> frame = console.build_frame().content("Test").build()
        """
        from styledconsole.builders import FrameBuilder

        return FrameBuilder()._bind_console(self)

    def build_banner(self) -> BannerBuilder:
        """Create a BannerBuilder for fluent banner construction.

        Returns a builder for ASCII art banners with figlet fonts.

        Returns:
            BannerBuilder instance bound to this console.

        Example:
            >>> console.build_banner().text("HELLO").font("slant").effect("fire").render()
        """
        from styledconsole.builders import BannerBuilder

        return BannerBuilder()._bind_console(self)

    def build_table(self) -> TableBuilder:
        """Create a TableBuilder for fluent table construction.

        Returns a builder for data tables with columns and rows.

        Returns:
            TableBuilder instance bound to this console.

        Example:
            >>> console.build_table().columns("Name", "Value").row("a", "1").row("b", "2").render()
        """
        from styledconsole.builders import TableBuilder

        return TableBuilder()._bind_console(self)

    def build_layout(self) -> LayoutBuilder:
        """Create a LayoutBuilder for fluent layout construction.

        Returns a builder for arranging multiple objects in layouts.

        Returns:
            LayoutBuilder instance bound to this console.

        Example:
            >>> from styledconsole.model import Text
            >>> console.build_layout().horizontal().gap(2).add(
            ...     Text(content="Left"), Text(content="Right")
            ... ).render()
        """
        from styledconsole.builders import LayoutBuilder

        return LayoutBuilder()._bind_console(self)

    # =========================================================================
    # Model Rendering (Phase 5 - v0.10.0 API)
    # =========================================================================

    def render_object(
        self,
        obj: ConsoleObject,
        *,
        context: RenderContext | None = None,
    ) -> None:
        """Render a ConsoleObject to the console.

        This method renders objects from the model layer (Text, Frame, Banner,
        Table, Layout, etc.) using the terminal renderer.

        Args:
            obj: ConsoleObject to render.
            context: Optional render context. If None, auto-detected.

        Example:
            >>> from styledconsole.model import Frame, Text
            >>> frame = Frame(content=Text(content="Hello"), title="Greeting")
            >>> console.render_object(frame)
        """
        from styledconsole.rendering import RenderContext, TerminalRenderer

        renderer = TerminalRenderer()
        ctx = context or RenderContext(
            color=self._policy.color,
            emoji=self._policy.emoji,
            width=self._rich_console.width,
        )
        renderer.render(obj, target=self._rich_console.file, context=ctx)

    # =========================================================================
    # Declarative Methods (Phase 5 - v0.10.0 API)
    # =========================================================================

    def render_dict(
        self,
        data: dict[str, Any] | list[Any] | str,
        *,
        variables: dict[str, Any] | None = None,
    ) -> None:
        """Render a ConsoleObject from declarative data.

        Supports shorthand syntax:
        - String: "Hello" renders as Text
        - List: ["a", "b"] renders as vertical Layout
        - Dict: {"frame": "content"} renders as Frame

        Args:
            data: Declarative data (dict, list, or string).
            variables: Optional template variables for ${var} substitution.

        Example:
            >>> console.render_dict("Hello World")
            >>> console.render_dict({"frame": "Content", "title": "Title"})
            >>> console.render_dict(["Item 1", "Item 2", "Item 3"])
        """
        from styledconsole.declarative import load_dict

        obj = load_dict(data, variables=variables)
        self.render_object(obj)

    def render_template(
        self,
        name: str,
        **variables: Any,
    ) -> None:
        """Render a named template with variable substitution.

        Uses built-in templates (info_box, warning_box, error_box, etc.)
        or custom registered templates.

        Args:
            name: Template name.
            **variables: Template variable values.

        Example:
            >>> console.render_template("info_box", message="Important information")
            >>> console.render_template("error_box", message="Something went wrong")
        """
        from styledconsole.declarative import Declarative

        decl = Declarative()
        obj = decl.from_template(name, **variables)
        self.render_object(obj)

    def render_file(
        self,
        path: str,
        *,
        variables: dict[str, Any] | None = None,
    ) -> None:
        """Render a ConsoleObject from a JSON or YAML file.

        Auto-detects format from file extension (.json, .yaml, .yml).

        Args:
            path: Path to the file.
            variables: Optional template variables.

        Example:
            >>> console.render_file("dashboard.yaml")
            >>> console.render_file("config.json", variables={"name": "Test"})
        """
        from styledconsole.declarative import load_file

        obj = load_file(path, variables=variables)
        self.render_object(obj)
