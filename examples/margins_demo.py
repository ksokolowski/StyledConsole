"""Demo of margins and frame alignment."""

from styledconsole import Console


def main():
    console = Console()

    console.print("\n=== Margin and Alignment Demo ===\n")

    # 1. Content Align vs Frame Align
    console.print("1. Content Align: Right, Frame Align: Left")
    console.frame(
        "Content is Right Aligned", align="right", frame_align="left", width=40, border="rounded"
    )

    console.print("\n2. Content Align: Left, Frame Align: Right")
    console.frame(
        "Content is Left Aligned", align="left", frame_align="right", width=40, border="rounded"
    )

    console.print("\n3. Content Align: Center, Frame Align: Center")
    console.frame(
        "Content is Center Aligned",
        align="center",
        frame_align="center",
        width=40,
        border="rounded",
    )

    # 2. Margins
    console.print("\n4. Left Margin (5 spaces)")
    console.frame("Left Margin: 5", margin=(0, 0, 0, 5), width=40, border="ascii")

    console.print("5. Top Margin (1 line) and Bottom Margin (1 line)")
    console.frame("Top and Bottom Margins", margin=(1, 0, 1, 0), width=40, border="ascii")
    console.print("(Gap should be visible above and below)")

    console.print("6. All Margins (2)")
    console.frame("Margin: 2", margin=2, width=40, border="double")

    # 3. Mixing Frame Align and Margin
    console.print("7. Center Frame with Left Margin (should shift/offset?)")
    console.print("Note: Margin adds space AROUND the frame. Then frame is aligned.")
    # If Frame Align is Center, and we add 10 left margin:
    # The block (margin + frame) is centered?
    # Or strict implementation: Margin is added to string, then rich aligns the string.
    console.frame(
        "Centered with Left Margin 10",
        frame_align="center",
        margin=(0, 0, 0, 10),
        width=30,
        border="solid",
    )


if __name__ == "__main__":
    main()
