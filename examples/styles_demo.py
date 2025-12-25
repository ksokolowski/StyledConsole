"""Demo of StyleContext and Presets."""

from styledconsole import ERROR_STYLE, SUCCESS_STYLE, WARNING_STYLE, Console, StyleContext


def main():
    console = Console()

    # 1. Using explicit StyleContext
    custom_style = StyleContext(
        border_style="double",
        border_color="cyan",
        title="Custom Style",
        title_color="cyan",
        padding=2,
        align="center",
    )

    console.frame("This frame uses a custom StyleContext object.", style=custom_style)

    # 2. Overriding StyleContext
    console.frame(
        "This frame uses the same style but overrides the border color to magenta.",
        style=custom_style,
        border_color="magenta",
        title="Overridden Style",
    )

    # 3. Using Presets
    console.frame("Operation Completed Successfully!", style=SUCCESS_STYLE)

    console.frame("Something went wrong!", style=ERROR_STYLE)

    console.frame("Disk space low.", style=WARNING_STYLE)

    # 4. Defaults fallback check (Backward Compatibility)
    console.frame("Standard Frame (should look like default)", title="Default")


if __name__ == "__main__":
    main()
