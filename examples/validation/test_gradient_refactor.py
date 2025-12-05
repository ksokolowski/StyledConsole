from styledconsole import THEMES, Console


def test_gradients():
    console = Console()

    print("\n=== VALIDATION: Gradient Refactor Baseline ===\n")

    # 1. Vertical Gradient (Content)
    print("1. Vertical Content Gradient (Red -> Blue)")
    console.frame(
        "Line 1\nLine 2\nLine 3\nLine 4",
        border="rounded",
        start_color="red",
        end_color="blue",
        title="Vertical Content",
    )

    # 2. Vertical Border Gradient
    print("\n2. Vertical Border Gradient (Green -> Yellow)")
    console.frame(
        "Content is plain",
        border="rounded",
        border_gradient_start="green",
        border_gradient_end="yellow",
        border_gradient_direction="vertical",
        title="Vertical Border",
    )

    # 3. Rainbow Theme (if supported by current engine via theme)
    print("\n3. Rainbow Theme (Vertical)")
    console = Console(theme=THEMES.RAINBOW)
    console.frame("Rainbow Content\nMulti-line", title="Rainbow Theme")


if __name__ == "__main__":
    test_gradients()
