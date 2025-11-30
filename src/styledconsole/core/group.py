"""Frame group context manager for nested frame layouts.

This module provides a context manager that captures frame() calls
and renders them together as a group when the context exits.

Example:
    >>> from styledconsole import Console
    >>> console = Console()
    >>> with console.group(title="Dashboard") as group:
    ...     console.frame("Section A", title="A")
    ...     console.frame("Section B", title="B")
    # Frames are captured and rendered together on context exit
"""

from __future__ import annotations

from contextvars import ContextVar
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from styledconsole.console import Console

# Context variable to track active group stack (thread-safe)
_active_groups: ContextVar[list[FrameGroupContext]] = ContextVar("_active_groups", default=[])


@dataclass
class CapturedFrame:
    """A captured frame call with all its arguments."""

    content: str | list[str]
    kwargs: dict[str, Any]
    rendered: str | None = None  # Cached rendered output


@dataclass
class FrameGroupContext:
    """Context manager for grouping multiple frames.

    When used as a context manager, captures all frame() calls made
    within the context and renders them together when the context exits.

    Attributes:
        console: The Console instance this group belongs to.
        title: Optional title for the outer frame.
        border: Border style for the outer frame.
        border_color: Border color for the outer frame.
        title_color: Title color for the outer frame.
        border_gradient_start: Gradient start color for outer border.
        border_gradient_end: Gradient end color for outer border.
        padding: Padding for the outer frame.
        width: Width for the outer frame.
        align: Alignment for content.
        gap: Lines between captured frames.
        inherit_style: Whether inner frames inherit outer style.
        align_widths: Whether to align all inner frame widths.
    """

    console: Console
    title: str | None = None
    border: str = "rounded"
    border_color: str | None = None
    title_color: str | None = None
    border_gradient_start: str | None = None
    border_gradient_end: str | None = None
    padding: int = 1
    width: int | None = None
    align: str = "left"
    gap: int = 1
    inherit_style: bool = False
    align_widths: bool = False

    # Internal state
    _captured_frames: list[CapturedFrame] = field(default_factory=list)
    _parent_group: FrameGroupContext | None = None

    def __enter__(self) -> FrameGroupContext:
        """Enter the context and start capturing frames."""
        # Get current stack (or create new one)
        stack = _active_groups.get()
        if stack is None:
            stack = []
            _active_groups.set(stack)

        # Track parent for nested groups
        if stack:
            self._parent_group = stack[-1]

        # Push this group onto the stack
        stack.append(self)
        _active_groups.set(stack)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        """Exit the context, render captured frames, and clean up."""
        # Pop this group from the stack
        stack = _active_groups.get()
        if stack and stack[-1] is self:
            stack.pop()
            _active_groups.set(stack)

        # Don't render if there was an exception
        if exc_type is not None:
            return False

        # Render the captured frames
        self._render_group()

        return False

    def capture_frame(
        self,
        content: str | list[str],
        **kwargs: Any,
    ) -> None:
        """Capture a frame call for later rendering.

        Args:
            content: The frame content.
            **kwargs: All frame() keyword arguments.
        """
        self._captured_frames.append(CapturedFrame(content=content, kwargs=kwargs))

    def _render_group(self) -> None:
        """Render all captured frames as a group."""
        if not self._captured_frames:
            # Empty group - just render outer frame if it has a title
            if self.title:
                self._output_to_parent_or_print("")
            return

        # Apply style inheritance if enabled
        if self.inherit_style:
            for frame in self._captured_frames:
                if "border" not in frame.kwargs:
                    frame.kwargs["border"] = self.border

        # Align widths if requested
        if self.align_widths:
            self._align_frame_widths()

        # Render each captured frame to string
        rendered_frames: list[str] = []
        for frame in self._captured_frames:
            rendered = self.console._renderer.render_frame_to_string(
                frame.content,
                **frame.kwargs,
            )
            rendered_frames.append(rendered)
            frame.rendered = rendered

        # Join with gap
        if self.gap > 0:
            gap_str = "\n" * self.gap
            combined = gap_str.join(rendered_frames)
        else:
            combined = "\n".join(rendered_frames)

        # Wrap in outer frame if we have any outer styling
        if self.title or self.border_color or self.border_gradient_start:
            output = self.console._renderer.render_frame_to_string(
                combined,
                title=self.title,
                border=self.border,
                border_color=self.border_color,
                title_color=self.title_color,
                border_gradient_start=self.border_gradient_start,
                border_gradient_end=self.border_gradient_end,
                padding=self.padding,
                width=self.width,
                align=self.align,
            )
        else:
            output = combined

        # Output to parent group or print
        self._output_to_parent_or_print(output)

    def _align_frame_widths(self) -> None:
        """Calculate and apply uniform width to all captured frames.

        Calculates the maximum width needed across all frames, considering
        both content width and title width, then applies that width uniformly.
        """
        from styledconsole.utils.text import visual_width

        # Calculate max width needed across all frames
        max_width = 0
        for frame in self._captured_frames:
            # Calculate content width
            content = frame.content
            if isinstance(content, str):
                lines = content.split("\n")
            else:
                lines = content

            content_width = 0
            for line in lines:
                # Use markup=True to handle Rich markup tags in content
                w = visual_width(line, markup=True)
                if w > content_width:
                    content_width = w

            # Calculate title width if present
            title = frame.kwargs.get("title", "")
            title_width = visual_width(title, markup=True) if title else 0

            # Frame needs to fit both content and title
            # Title appears in border, so it needs ~4 extra chars for decoration
            effective_title_width = title_width + 4 if title else 0
            # Content needs padding (default 1 on each side = 2)
            effective_content_width = content_width + 2

            frame_inner_width = max(effective_content_width, effective_title_width)
            if frame_inner_width > max_width:
                max_width = frame_inner_width

        # Add border characters (2 for left+right)
        frame_width = max_width + 2

        # Apply width to all frames that don't have explicit width
        for frame in self._captured_frames:
            if frame.kwargs.get("width") is None:
                frame.kwargs["width"] = frame_width

    def _output_to_parent_or_print(self, output: str) -> None:
        """Output to parent group (if nested) or print directly."""
        if self._parent_group is not None:
            # We're nested - capture as a single "frame" in parent
            self._parent_group._captured_frames.append(
                CapturedFrame(content=output, kwargs={}, rendered=output)
            )
        else:
            # Top-level group - print the output
            self.console._print_ansi_output(output, self.align)


def get_active_group() -> FrameGroupContext | None:
    """Get the currently active group context, if any.

    Returns:
        The innermost active FrameGroupContext, or None if not in a group context.
    """
    stack = _active_groups.get()
    if stack:
        return stack[-1]
    return None


def is_capturing() -> bool:
    """Check if we're currently inside a group context.

    Returns:
        True if frame() calls should be captured, False if they should print.
    """
    return get_active_group() is not None
