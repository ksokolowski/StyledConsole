"""HTMLRenderer - renders ConsoleObjects to HTML.

This renderer generates HTML output directly, without going through ANSI.
It supports two output modes:
- Fragment: HTML elements only (for embedding in existing pages)
- Document: Complete HTML file with CSS

Example:
    >>> from styledconsole.rendering import HTMLRenderer
    >>> from styledconsole.model import Frame, Text
    >>>
    >>> renderer = HTMLRenderer()
    >>> frame = Frame(content=Text(content="Hello"), title="Greeting")
    >>>
    >>> # Get HTML fragment for embedding
    >>> html = renderer.render_fragment(frame)
    >>>
    >>> # Create complete HTML document
    >>> renderer.render_document(frame, "output.html")
"""

from __future__ import annotations

import html
from typing import IO, TYPE_CHECKING, Any, Literal

from styledconsole.rendering.base import BaseRenderer

if TYPE_CHECKING:
    from styledconsole.model import (
        Banner,
        Frame,
        Group,
        Layout,
        Rule,
        Spacer,
        Style,
        Table,
        Text,
    )
    from styledconsole.rendering.context import RenderContext


class HTMLRenderer(BaseRenderer):
    """Renders ConsoleObjects to HTML.

    Supports two output modes:
    - Fragment: HTML elements only (for embedding)
    - Document: Complete HTML file with embedded CSS

    Style modes:
    - "inline": Styles as style="" attributes (safe for embedding)
    - "classes": CSS class names (cleaner HTML, requires stylesheet)

    Example:
        >>> renderer = HTMLRenderer(style_mode="inline")
        >>> html = renderer.render_fragment(frame)
        >>> renderer.render_document(dashboard, "report.html")
    """

    def __init__(self, style_mode: Literal["inline", "classes"] = "inline") -> None:
        """Initialize the HTML renderer.

        Args:
            style_mode: How to apply CSS styling:
                - "inline": Embed styles in style="" attributes
                - "classes": Use CSS class names
        """
        self._style_mode = style_mode

    def _default_context(self) -> RenderContext:
        """Default context for HTML rendering."""
        from styledconsole.rendering.context import RenderContext

        return RenderContext.for_html()

    def render(
        self,
        obj: Any,
        target: str | IO[str] | None = None,
        context: RenderContext | None = None,
    ) -> str:
        """Convenience method: document if target provided, else fragment.

        Args:
            obj: ConsoleObject to render.
            target: File path or file-like object. None for fragment only.
            context: Rendering context.

        Returns:
            HTML string (fragment or document).
        """
        if target:
            return self.render_document(obj, target, context)
        return self.render_fragment(obj, context)

    def render_fragment(
        self,
        obj: Any,
        context: RenderContext | None = None,
    ) -> str:
        """Render ConsoleObject to HTML fragment.

        Returns only the HTML elements, suitable for embedding in
        existing HTML documents.

        Args:
            obj: ConsoleObject to render.
            context: Rendering context.

        Returns:
            HTML fragment string.
        """
        ctx = self._get_context(context)
        result = self._dispatch(obj, ctx)
        return str(result) if result else ""

    def render_document(
        self,
        obj: Any,
        target: str | IO[str] | None = None,
        context: RenderContext | None = None,
        title: str = "StyledConsole Output",
    ) -> str:
        """Render to complete HTML document.

        Wraps the fragment in full HTML structure with embedded CSS.

        Args:
            obj: ConsoleObject to render.
            target: File path or file-like object.
            context: Rendering context.
            title: HTML document title.

        Returns:
            Complete HTML document string.
        """
        ctx = self._get_context(context)
        fragment = self.render_fragment(obj, ctx)

        document = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{html.escape(title)}</title>
    <style>
{self._get_stylesheet(ctx)}
    </style>
</head>
<body>
    <div class="styled-console">
{fragment}
    </div>
</body>
</html>"""

        if isinstance(target, str):
            with open(target, "w", encoding="utf-8") as f:
                f.write(document)
        elif target is not None:
            target.write(document)

        return document

    def _render_text(self, obj: Text, context: RenderContext) -> str:
        """Render Text to HTML span."""
        content = html.escape(obj.content)
        style = self._style_to_css(obj.style) if obj.style else ""

        if style:
            return f'<span style="{style}">{content}</span>'
        return f"<span>{content}</span>"

    def _render_frame(self, obj: Frame, context: RenderContext) -> str:
        """Render Frame to HTML div."""
        content = self._dispatch(obj.content, context) if obj.content else ""

        border_style = self._get_border_css(obj.border, obj.effect)
        padding_style = f"padding: {obj.padding * 8}px;"

        if self._style_mode == "inline":
            style = f"{border_style} {padding_style} margin: 8px 0; font-family: monospace;"

            title_html = ""
            if obj.title:
                escaped_title = html.escape(obj.title)
                title_style = "font-weight: bold; margin-bottom: 4px;"
                title_html = f'<div style="{title_style}">{escaped_title}</div>'

            return f"""<div style="{style}">
    {title_html}
    <div>{content}</div>
</div>"""
        else:
            classes = ["styled-frame", f"border-{obj.border}"]
            if obj.effect:
                classes.append(f"effect-{obj.effect}")

            title_html = ""
            if obj.title:
                title_html = f'<div class="frame-title">{html.escape(obj.title)}</div>'

            return f"""<div class="{" ".join(classes)}">
    {title_html}
    <div class="frame-content">{content}</div>
</div>"""

    def _render_banner(self, obj: Banner, context: RenderContext) -> str:
        """Render Banner to HTML pre."""
        import pyfiglet

        figlet = pyfiglet.Figlet(font=obj.font, width=context.width)
        ascii_art = html.escape(figlet.renderText(obj.text))

        color = self._effect_to_color(obj.effect) if obj.effect else None
        style = f"color: {color};" if color else ""

        if self._style_mode == "inline":
            return f'<pre style="font-family: monospace; {style}">{ascii_art}</pre>'
        else:
            classes = ["styled-banner"]
            if obj.effect:
                classes.append(f"effect-{obj.effect}")
            return f'<pre class="{" ".join(classes)}">{ascii_art}</pre>'

    def _render_table(self, obj: Table, context: RenderContext) -> str:
        """Render Table to HTML table."""
        border_color = self._effect_to_color(obj.effect) if obj.effect else "#ccc"

        if self._style_mode == "inline":
            style = f"border-collapse: collapse; border: 1px solid {border_color};"
            th_style = f"border: 1px solid {border_color}; padding: 8px; text-align: left;"
            td_style = f"border: 1px solid {border_color}; padding: 8px;"

            # Build header
            headers = "".join(
                f'<th style="{th_style}">{html.escape(col.header)}</th>' for col in obj.columns
            )

            # Build rows
            rows = []
            for row in obj.rows:
                cells = "".join(
                    f'<td style="{td_style}">{html.escape(str(cell))}</td>' for cell in row
                )
                rows.append(f"<tr>{cells}</tr>")

            title_html = ""
            if obj.title:
                escaped = html.escape(obj.title)
                caption_style = "font-weight: bold; margin-bottom: 8px;"
                title_html = f'<caption style="{caption_style}">{escaped}</caption>'

            return f"""<table style="{style}">
    {title_html}
    <thead><tr>{headers}</tr></thead>
    <tbody>{"".join(rows)}</tbody>
</table>"""
        else:
            classes = ["styled-table"]
            if obj.effect:
                classes.append(f"effect-{obj.effect}")

            headers = "".join(f"<th>{html.escape(col.header)}</th>" for col in obj.columns)

            rows = []
            for row in obj.rows:
                cells = "".join(f"<td>{html.escape(str(cell))}</td>" for cell in row)
                rows.append(f"<tr>{cells}</tr>")

            title_html = ""
            if obj.title:
                title_html = f"<caption>{html.escape(obj.title)}</caption>"

            return f"""<table class="{" ".join(classes)}">
    {title_html}
    <thead><tr>{headers}</tr></thead>
    <tbody>{"".join(rows)}</tbody>
</table>"""

    def _render_layout(self, obj: Layout, context: RenderContext) -> str:
        """Render Layout to HTML div."""
        if not obj.children:
            return '<div class="styled-layout"></div>'

        children_html = [self._dispatch(child, context) for child in obj.children]

        gap_px = obj.gap * 8
        if obj.direction == "horizontal":
            style = f"display: flex; gap: {gap_px}px;"
        elif obj.direction == "grid":
            cols = obj.columns or 2
            grid_cols = f"repeat({cols}, 1fr)"
            style = f"display: grid; grid-template-columns: {grid_cols}; gap: {gap_px}px;"
        else:  # vertical
            style = f"display: flex; flex-direction: column; gap: {gap_px}px;"

        children_str = "".join(children_html)
        if self._style_mode == "inline":
            return f'<div style="{style}">{children_str}</div>'
        else:
            cls = f"styled-layout layout-{obj.direction}"
            return f'<div class="{cls}">{children_str}</div>'

    def _render_group(self, obj: Group, context: RenderContext) -> str:
        """Render Group to HTML div."""
        if not obj.children:
            return '<div class="styled-group"></div>'

        children_html = [self._dispatch(child, context) for child in obj.children]
        return f'<div class="styled-group">{"".join(children_html)}</div>'

    def _render_spacer(self, obj: Spacer, context: RenderContext) -> str:
        """Render Spacer to HTML div."""
        height = obj.lines * 16  # Approximate line height
        if self._style_mode == "inline":
            return f'<div style="height: {height}px;"></div>'
        return f'<div class="styled-spacer" style="height: {height}px;"></div>'

    def _render_rule(self, obj: Rule, context: RenderContext) -> str:
        """Render Rule to HTML hr."""
        if obj.title:
            if self._style_mode == "inline":
                return f"""<div style="display: flex; align-items: center; margin: 16px 0;">
    <hr style="flex: 1; border: none; border-top: 1px solid #ccc;">
    <span style="padding: 0 16px;">{html.escape(obj.title)}</span>
    <hr style="flex: 1; border: none; border-top: 1px solid #ccc;">
</div>"""
            return f"""<div class="styled-rule">
    <hr><span>{html.escape(obj.title)}</span><hr>
</div>"""
        return '<hr style="border: none; border-top: 1px solid #ccc; margin: 16px 0;">'

    # Helper methods

    def _style_to_css(self, style: Style) -> str:
        """Convert model Style to CSS string."""
        parts = []
        if style.color:
            parts.append(f"color: {style.color}")
        if style.background:
            parts.append(f"background-color: {style.background}")
        if style.bold:
            parts.append("font-weight: bold")
        if style.italic:
            parts.append("font-style: italic")
        if style.underline:
            parts.append("text-decoration: underline")
        if style.dim:
            parts.append("opacity: 0.6")
        if style.strikethrough:
            parts.append("text-decoration: line-through")
        return "; ".join(parts)

    def _get_border_css(self, border: str, effect: str | None) -> str:
        """Get CSS border style."""
        color = self._effect_to_color(effect) if effect else "#ccc"

        border_styles = {
            "solid": f"border: 1px solid {color};",
            "rounded": f"border: 1px solid {color}; border-radius: 8px;",
            "heavy": f"border: 2px solid {color};",
            "double": f"border: 3px double {color};",
            "simple": f"border-top: 1px solid {color}; border-bottom: 1px solid {color};",
            "minimal": "",
            "none": "",
        }
        return border_styles.get(border, f"border: 1px solid {color};")

    def _effect_to_color(self, effect: str | None) -> str:
        """Map effect name to CSS color."""
        if not effect:
            return "#ccc"

        effect_colors = {
            "ocean": "#00d4ff",
            "fire": "#ff4444",
            "forest": "#44ff44",
            "sunset": "#ffaa00",
            "steel": "#888888",
            "rainbow": "#ff00ff",
            "neon": "#ff00ff",
            "aurora": "#00ffff",
        }
        return effect_colors.get(effect, "#ccc")

    def _get_stylesheet(self, context: RenderContext) -> str:
        """Get CSS stylesheet for document mode."""
        bg = context.background_color
        return f"""        body {{
            background-color: {bg};
            color: #f0f0f0;
            font-family: 'JetBrains Mono', 'Consolas', monospace;
            padding: 20px;
            margin: 0;
        }}
        .styled-console {{
            max-width: {context.width}ch;
            margin: 0 auto;
        }}
        .styled-frame {{
            border: 1px solid #ccc;
            border-radius: 8px;
            padding: 8px;
            margin: 8px 0;
        }}
        .styled-frame .frame-title {{
            font-weight: bold;
            margin-bottom: 4px;
        }}
        .styled-table {{
            border-collapse: collapse;
            width: 100%;
            margin: 8px 0;
        }}
        .styled-table th, .styled-table td {{
            border: 1px solid #ccc;
            padding: 8px;
            text-align: left;
        }}
        .styled-banner {{
            font-family: monospace;
            white-space: pre;
        }}
        .styled-rule {{
            display: flex;
            align-items: center;
            margin: 16px 0;
        }}
        .styled-rule hr {{
            flex: 1;
            border: none;
            border-top: 1px solid #ccc;
        }}
        .styled-rule span {{
            padding: 0 16px;
        }}
        .effect-ocean {{ border-color: #00d4ff !important; color: #00d4ff; }}
        .effect-fire {{ border-color: #ff4444 !important; color: #ff4444; }}
        .effect-forest {{ border-color: #44ff44 !important; color: #44ff44; }}
        .effect-sunset {{ border-color: #ffaa00 !important; color: #ffaa00; }}
        .effect-steel {{ border-color: #888888 !important; color: #888888; }}
        .effect-rainbow {{ border-color: #ff00ff !important; color: #ff00ff; }}
        .effect-neon {{ border-color: #ff00ff !important; color: #ff00ff; }}
        .effect-aurora {{ border-color: #00ffff !important; color: #00ffff; }}
"""


__all__ = ["HTMLRenderer"]
