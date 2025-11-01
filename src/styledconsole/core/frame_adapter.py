"""Frame adapter for backward compatibility.

Provides FrameAdapter class that wraps RenderingEngine for legacy FrameRenderer API.

.. deprecated:: 0.4.0
    The legacy methods in this module are deprecated and will be removed in v1.0.0.
"""

from __future__ import annotations

from io import StringIO
from typing import TYPE_CHECKING

from rich.console import Console as RichConsole

if TYPE_CHECKING:
    from styledconsole.core.styles import BorderStyle


class FrameAdapter:
    """Adapts legacy FrameRenderer API to Rich Panel rendering.

    This adapter captures output from RenderingEngine.print_frame()
    and returns it as a list of strings, maintaining backward
    compatibility with the legacy FrameRenderer.render() API.

    v0.4.0: Replaces FrameRenderer implementation
    v1.0.0: FrameRenderer class removed entirely
    """

    def __init__(self) -> None:
        """Initialize the frame adapter.

        Creates internal rendering engine for delegation.
        """
        # Lazy import to avoid circular dependency
        from styledconsole.core.rendering_engine import RenderingEngine

        # Create buffer for capturing output
        self._buffer = StringIO()

        # Create Rich console writing to buffer
        self._rich_console = RichConsole(
            file=self._buffer,
            record=False,
            force_terminal=True,  # Enable ANSI codes
            force_jupyter=False,
            force_interactive=False,
            width=999,  # Wide enough to not wrap
            height=999,
        )

        # Create rendering engine
        self._engine = RenderingEngine(self._rich_console, debug=False)

    def render(
        self,
        content: str | list[str],
        title: str | None = None,
        border: str | BorderStyle = "solid",
        width: int | None = None,
        padding: int = 1,
        align: str = "left",
        min_width: int = 20,
        max_width: int = 100,
        content_color: str | None = None,
        border_color: str | None = None,
        title_color: str | None = None,
        start_color: str | None = None,
        end_color: str | None = None,
    ) -> list[str]:
        """Render a frame and return as list of strings.

        This method delegates to RenderingEngine.print_frame(),
        captures the output, and returns it as a list of lines.

        Args:
            content: Text content (single line or list of lines)
            title: Optional title for the top border
            border: Border style name or BorderStyle object
            width: Frame width (auto-calculated if None)
            padding: Internal padding (left/right spaces)
            align: Content alignment ("left", "center", "right")
            min_width: Minimum frame width (when auto-calculating)
            max_width: Maximum frame width (when auto-calculating)
            content_color: Color for content text (hex, rgb, or CSS4 name)
            border_color: Color for border (hex, rgb, or CSS4 name)
            title_color: Color for title (hex, rgb, or CSS4 name)
            start_color: Starting color for content gradient (overrides content_color)
            end_color: Ending color for content gradient

        Returns:
            List of strings, one per line of the rendered frame
        """
        from styledconsole.utils.text import visual_width

        # Reset buffer
        self._buffer.seek(0)
        self._buffer.truncate(0)

        # Convert BorderStyle to string if needed
        if hasattr(border, "name"):
            border_name = border.name
        else:
            border_name = str(border)

        # Normalize content to list of lines for width calculation
        if isinstance(content, str):
            content_lines = content.splitlines() if content else [""]
        else:
            content_lines = list(content) if content else [""]

        # Calculate width if not provided
        if width is None:
            # Find longest content line
            max_content_width = 0
            for line in content_lines:
                content_width = visual_width(line)
                if content_width > max_content_width:
                    max_content_width = content_width

            # Account for borders (2 chars) + padding (both sides)
            needed_width = max_content_width + 2 + (padding * 2)

            # Check title width if present
            if title:
                # Title needs space for " title " + borders
                title_width = visual_width(title) + 2 + 2  # spaces + borders
                needed_width = max(needed_width, title_width)

            # Clamp to min/max
            width = max(min_width, min(needed_width, max_width))

        # When width is specified, pad content to ensure Rich Panel respects it
        if width:
            # Calculate content area width (excluding borders and padding)
            content_area_width = width - 2 - (padding * 2)
            if content_area_width > 0:
                # Pad each content line to fill the content area
                from styledconsole.utils.text import pad_to_width, truncate_to_width

                padded_lines = []
                for line in content_lines:
                    # Truncate if too long, then pad to exact width
                    truncated = truncate_to_width(line, content_area_width)
                    padded = pad_to_width(truncated, content_area_width, align=align)
                    padded_lines.append(padded)
                # Replace content with padded version (as string for RenderingEngine)
                content = "\n".join(padded_lines)

        # Delegate to RenderingEngine.print_frame()
        self._engine.print_frame(
            content,
            title=title,
            border=border_name,
            width=width,
            padding=padding,
            align=align,
            content_color=content_color,
            border_color=border_color,
            title_color=title_color,
            start_color=start_color,
            end_color=end_color,
        )

        # Get output from buffer
        output = self._buffer.getvalue()

        # Return as list of lines (legacy format)
        return output.splitlines()

    def render_frame(self, frame) -> list[str]:
        """Render a Frame dataclass.

        This is a convenience method that extracts fields from a Frame
        dataclass and delegates to render().

        Args:
            frame: Frame dataclass with rendering configuration

        Returns:
            List of strings, one per line of the rendered frame
        """
        return self.render(
            content=frame.content,
            title=frame.title,
            border=frame.border,
            width=frame.width,
            padding=frame.padding,
            align=frame.align,
            min_width=frame.min_width,
            max_width=frame.max_width,
            content_color=frame.content_color,
            border_color=frame.border_color,
            title_color=frame.title_color,
            start_color=frame.start_color,
            end_color=frame.end_color,
        )
