"""Text wrapping utilities for frames with variable-length content.

This module provides helpers for intelligently wrapping long text content
into frames, handling word breaks, preserving formatting, and managing
error logs or dynamic content.
"""

import textwrap

from styledconsole.types import AlignType
from styledconsole.utils.text import visual_width


def wrap_text(
    text: str,
    width: int,
    *,
    break_long_words: bool = True,
    break_on_hyphens: bool = True,
    preserve_paragraphs: bool = False,
) -> list[str]:
    """Wrap text to fit within specified width.

    Args:
        text: Text to wrap
        width: Maximum line width
        break_long_words: Break words longer than width
        break_on_hyphens: Break on hyphens
        preserve_paragraphs: Preserve empty lines as paragraph breaks

    Returns:
        List of wrapped lines

    Example:
        >>> text = "This is a very long line that needs to be wrapped"
        >>> lines = wrap_text(text, width=20)
        >>> for line in lines:
        ...     print(line)
        This is a very long
        line that needs to
        be wrapped
    """
    if not text:
        return [""]

    if preserve_paragraphs:
        # Process each paragraph separately
        paragraphs = text.split("\n\n")
        result = []
        for i, para in enumerate(paragraphs):
            wrapped = textwrap.wrap(
                para.strip(),
                width=width,
                break_long_words=break_long_words,
                break_on_hyphens=break_on_hyphens,
            )
            result.extend(wrapped or [""])
            # Add blank line between paragraphs (except after last)
            if i < len(paragraphs) - 1:
                result.append("")
        return result
    else:
        # Wrap as single block
        wrapped = textwrap.wrap(
            text,
            width=width,
            break_long_words=break_long_words,
            break_on_hyphens=break_on_hyphens,
        )
        return wrapped or [""]


def wrap_multiline(
    lines: list[str],
    width: int,
    *,
    break_long_words: bool = True,
    preserve_indentation: bool = True,
) -> list[str]:
    """Wrap multiple lines of text, preserving line breaks.

    Args:
        lines: List of text lines to wrap
        width: Maximum line width
        break_long_words: Break words longer than width
        preserve_indentation: Preserve leading whitespace

    Returns:
        List of wrapped lines

    Example:
        >>> lines = [
        ...     "First line is short",
        ...     "  Second line is indented and very long so it wraps",
        ...     "Third line"
        ... ]
        >>> wrapped = wrap_multiline(lines, width=20)
    """
    result = []

    for line in lines:
        if not line.strip():
            # Preserve empty lines
            result.append("")
            continue

        # Detect indentation
        indent = ""
        if preserve_indentation:
            indent = line[: len(line) - len(line.lstrip())]

        # Wrap the line
        wrapped = textwrap.wrap(
            line.strip(),
            width=width - len(indent),
            initial_indent=indent,
            subsequent_indent=indent,
            break_long_words=break_long_words,
        )

        result.extend(wrapped or [indent])

    return result


def truncate_lines(
    lines: list[str],
    max_lines: int,
    *,
    truncation_indicator: str = "... ({count} more lines)",
) -> list[str]:
    """Truncate a list of lines with an indicator.

    Args:
        lines: Lines to potentially truncate
        max_lines: Maximum number of lines to keep (if <= 0, no truncation)
        truncation_indicator: Message to show when truncated.
            Use {count} to show number of omitted lines.

    Returns:
        Truncated list with indicator if needed

    Example:
        >>> lines = [f"Line {i}" for i in range(100)]
        >>> truncated = truncate_lines(lines, max_lines=5)
        >>> print(truncated[-1])
        ... (95 more lines)
    """
    # No truncation if max_lines is <= 0 or lines fit within limit
    if max_lines <= 0 or len(lines) <= max_lines:
        return lines

    omitted_count = len(lines) - max_lines
    indicator = truncation_indicator.format(count=omitted_count)

    return lines[:max_lines] + [indicator]


def prepare_frame_content(
    text: str | list[str],
    *,
    max_width: int = 80,
    max_lines: int | None = None,
    wrap: bool = True,
    break_long_words: bool = True,
    preserve_paragraphs: bool = False,
) -> list[str]:
    """Prepare content for framing with intelligent wrapping and truncation.

    This is the main helper function for variable-length content. It handles:
    - Text wrapping to fit width
    - Line truncation with indicators
    - Paragraph preservation
    - Word breaking

    Args:
        text: Content as string or list of lines
        max_width: Maximum width for content (excludes frame borders/padding)
        max_lines: Maximum number of lines (truncate with indicator if exceeded)
        wrap: Enable text wrapping
        break_long_words: Break words that exceed width
        preserve_paragraphs: Preserve paragraph breaks (double newlines)

    Returns:
        List of prepared lines ready for framing

    Example:
        >>> # Long error message
        >>> error = "FileNotFoundError: The file '/path/to/very/long/filename.txt' "\
        ...         "could not be found"
        >>> content = prepare_frame_content(error, max_width=40)
        >>> # Content is now wrapped to 40 chars per line
    """
    # Normalize to list of lines
    if isinstance(text, str):
        lines = [text]
    else:
        lines = text if text else [""]  # Handle empty list

    # Apply wrapping if enabled
    if wrap:
        wrapped_lines = []
        for line in lines:
            if not line.strip():
                wrapped_lines.append("")
            else:
                wrapped = wrap_text(
                    line,
                    max_width,
                    break_long_words=break_long_words,
                    preserve_paragraphs=preserve_paragraphs,
                )
                wrapped_lines.extend(wrapped)
        lines = wrapped_lines

    # Apply line truncation if specified
    if max_lines is not None:
        lines = truncate_lines(lines, max_lines)

    return lines


def auto_size_content(
    text: str | list[str],
    *,
    max_width: int = 100,
    min_width: int = 20,
    max_lines: int | None = None,
) -> tuple[list[str], int]:
    """Automatically determine optimal width and prepare content.

    This function analyzes content and determines the best width,
    then wraps content accordingly. Useful for dynamic content
    where you want the frame to be "just right".

    Args:
        text: Content to analyze
        max_width: Maximum allowed width
        min_width: Minimum desired width
        max_lines: Maximum number of lines

    Returns:
        Tuple of (prepared_lines, optimal_width)

    Example:
        >>> error_log = "ERROR: Something went wrong..."
        >>> lines, width = auto_size_content(error_log)
        >>> # Use lines and width with Console.frame()
    """
    # Normalize to list
    if isinstance(text, str):
        lines = text.splitlines() if text else [""]
    else:
        lines = text

    # Calculate optimal width based on content
    max_line_width = 0
    for line in lines:
        line_width = visual_width(line)
        max_line_width = max(max_line_width, line_width)

    # Determine optimal width
    if max_line_width <= max_width:
        # Content fits, use its natural width
        optimal_width = max(min_width, max_line_width)
        prepared_lines = lines
    else:
        # Content too wide, wrap to max_width
        optimal_width = max_width
        prepared_lines = prepare_frame_content(
            lines, max_width=max_width, wrap=True, max_lines=max_lines
        )

    return prepared_lines, optimal_width


__all__ = [
    "wrap_text",
    "wrap_multiline",
    "truncate_lines",
    "prepare_frame_content",
    "auto_size_content",
    "AlignType",
]
