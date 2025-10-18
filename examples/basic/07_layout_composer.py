"""Layout Composer Examples

Demonstrates the layout composition capabilities for creating
complex multi-section displays using vertical stacking, grids,
and side-by-side placement.
"""

from styledconsole import (
    BannerRenderer,
    FrameRenderer,
    Layout,
    LayoutComposer,
)


def example_1_basic_stacking():
    """Example 1: Basic vertical stacking with spacing."""
    print("\n" + "=" * 60)
    print("Example 1: Basic Vertical Stacking")
    print("=" * 60 + "\n")

    composer = LayoutComposer()
    frame_renderer = FrameRenderer()

    # Create three sections
    header = frame_renderer.render(["Application Dashboard"], title="Header")
    content = frame_renderer.render(
        ["This is the main content area", "Multiple lines supported"], title="Content"
    )
    footer = frame_renderer.render(["Status: Active"], title="Footer")

    # Stack them with spacing
    result = composer.stack([header, content, footer], spacing=1)

    for line in result:
        print(line)


def example_2_side_by_side():
    """Example 2: Side-by-side placement."""
    print("\n" + "=" * 60)
    print("Example 2: Side-by-Side Placement")
    print("=" * 60 + "\n")

    composer = LayoutComposer()
    frame_renderer = FrameRenderer()

    # Create left and right panels
    left_panel = frame_renderer.render(["Option 1", "Option 2", "Option 3"], title="Menu")
    right_panel = frame_renderer.render(
        ["Details about", "the selected", "option"], title="Details"
    )

    # Place side by side
    result = composer.side_by_side(left_panel, right_panel, spacing=3)

    for line in result:
        print(line)


def example_3_grid_layout():
    """Example 3: Grid layout with 2x2 cells."""
    print("\n" + "=" * 60)
    print("Example 3: Grid Layout (2x2)")
    print("=" * 60 + "\n")

    composer = LayoutComposer()
    frame_renderer = FrameRenderer()

    # Create 2x2 grid of status cards
    row1 = [
        frame_renderer.render(["Count: 42"], title="Users"),
        frame_renderer.render(["Count: 128"], title="Posts"),
    ]

    row2 = [
        frame_renderer.render(["Count: 5"], title="Admins"),
        frame_renderer.render(["Count: 3"], title="Alerts"),
    ]

    # Create grid
    result = composer.grid([row1, row2], column_spacing=2, row_spacing=1)

    for line in result:
        print(line)


def example_4_alignment_options():
    """Example 4: Different alignment options."""
    print("\n" + "=" * 60)
    print("Example 4: Alignment Options")
    print("=" * 60 + "\n")

    composer = LayoutComposer()

    elements = [["Short"], ["Much longer text line"], ["Mid"]]

    # Left alignment
    print("Left Aligned:")
    result = composer.stack(elements, align="left", spacing=0)
    for line in result:
        print(f"  {line}")

    print("\nCenter Aligned:")
    result = composer.stack(elements, align="center", spacing=0)
    for line in result:
        print(f"  {line}")

    print("\nRight Aligned:")
    result = composer.stack(elements, align="right", spacing=0)
    for line in result:
        print(f"  {line}")


def example_5_layout_object():
    """Example 5: Using Layout dataclass."""
    print("\n" + "=" * 60)
    print("Example 5: Layout Object")
    print("=" * 60 + "\n")

    composer = LayoutComposer()
    frame_renderer = FrameRenderer()

    # Create elements
    elem1 = frame_renderer.render(["Section 1"], title="A")
    elem2 = frame_renderer.render(["Section 2"], title="B")
    elem3 = frame_renderer.render(["Section 3"], title="C")

    # Create Layout configuration
    layout = Layout(
        elements=[elem1, elem2, elem3],
        spacing=2,
        align="center",
        width=50,
    )

    # Render the layout
    result = composer.compose(layout)

    for line in result:
        print(line)


def example_6_complex_dashboard():
    """Example 6: Complex dashboard with nested layouts."""
    print("\n" + "=" * 60)
    print("Example 6: Complex Dashboard")
    print("=" * 60 + "\n")

    composer = LayoutComposer()
    frame_renderer = FrameRenderer()
    banner_renderer = BannerRenderer()

    # Title banner
    title = banner_renderer.render("DASHBOARD", font="banner")

    # Stats grid
    stats = [
        [
            frame_renderer.render(["1,234"], title="📊 Users"),
            frame_renderer.render(["567"], title="📝 Posts"),
            frame_renderer.render(["89"], title="💬 Comments"),
        ]
    ]
    stats_grid = composer.grid(stats, column_spacing=2)

    # Main content
    content = frame_renderer.render(
        ["Welcome to the dashboard", "All systems operational"],
        title="Status",
    )

    # Footer
    footer = frame_renderer.render(["Last updated: 2025-10-18"], title="Info")

    # Combine all sections
    result = composer.stack([title, stats_grid, content, footer], spacing=1)

    for line in result:
        print(line)


def example_7_three_column_layout():
    """Example 7: Three-column layout."""
    print("\n" + "=" * 60)
    print("Example 7: Three-Column Layout")
    print("=" * 60 + "\n")

    composer = LayoutComposer()
    frame_renderer = FrameRenderer()

    # Create three columns
    col1 = frame_renderer.render(["Column", "One"], title="Left")
    col2 = frame_renderer.render(["Column", "Two"], title="Center")
    col3 = frame_renderer.render(["Column", "Three"], title="Right")

    # Create single row with three columns
    row = [col1, col2, col3]
    result = composer.grid([row], column_spacing=1)

    for line in result:
        print(line)


def example_8_nested_composition():
    """Example 8: Nested composition."""
    print("\n" + "=" * 60)
    print("Example 8: Nested Composition")
    print("=" * 60 + "\n")

    composer = LayoutComposer()
    frame_renderer = FrameRenderer()

    # Create header
    header = frame_renderer.render(["Application"], title="Title")

    # Create nested side-by-side section
    left = frame_renderer.render(["Menu Item 1", "Menu Item 2"], title="Navigation")
    right = frame_renderer.render(["Content Area", "Details here"], title="Main")
    middle_section = composer.side_by_side(left, right, spacing=2)

    # Create footer
    footer = frame_renderer.render(["© 2025"], title="Footer")

    # Combine everything
    result = composer.stack([header, middle_section, footer], spacing=1)

    for line in result:
        print(line)


def example_9_emoji_safe_alignment():
    """Example 9: Emoji-safe alignment."""
    print("\n" + "=" * 60)
    print("Example 9: Emoji-Safe Alignment")
    print("=" * 60 + "\n")

    composer = LayoutComposer()

    elements = [["🚀 Rocket"], ["⭐ Star"], ["💎 Gem"], ["🎯 Target"]]

    # Stack with center alignment
    result = composer.stack(elements, align="center", spacing=0, width=30)

    for line in result:
        print(f"  |{line}|")


def example_10_custom_spacing():
    """Example 10: Custom spacing between elements."""
    print("\n" + "=" * 60)
    print("Example 10: Custom Spacing")
    print("=" * 60 + "\n")

    composer = LayoutComposer()
    frame_renderer = FrameRenderer()

    elements = [
        frame_renderer.render(["Section A"], title="A"),
        frame_renderer.render(["Section B"], title="B"),
        frame_renderer.render(["Section C"], title="C"),
    ]

    print("No spacing:")
    result = composer.stack(elements, spacing=0)
    for line in result:
        print(line)

    print("\n\nWith 3 lines spacing:")
    result = composer.stack(elements, spacing=3)
    for line in result:
        print(line)


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("LAYOUT COMPOSER EXAMPLES")
    print("=" * 60)

    example_1_basic_stacking()
    example_2_side_by_side()
    example_3_grid_layout()
    example_4_alignment_options()
    example_5_layout_object()
    example_6_complex_dashboard()
    example_7_three_column_layout()
    example_8_nested_composition()
    example_9_emoji_safe_alignment()
    example_10_custom_spacing()

    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60 + "\n")
