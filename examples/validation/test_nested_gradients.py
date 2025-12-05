from styledconsole.effects import gradient_frame


def main():
    print("\n=== REPRODUCTION: Nested Gradients ===\n")

    # Inner frame with its own gradient (Red -> Yellow)
    inner_lines = gradient_frame(
        ["Inner Content Line 1", "Inner Content Line 2"],
        start_color="red",
        end_color="yellow",
        border="double",
        title="Inner",
    )
    # Join inner lines to pass as content string to outer frame,
    # OR pass as list of strings if the API supports it.
    # The gradient_frame API takes str or list[str].
    # If we pass a list of strings (which already have ANSI codes),
    # the outer frame should respect them or at least not break them if it's applying
    # a border gradient.

    # Outer frame with a different gradient (Blue -> Cyan)
    # If the user says "Only most outer frames gets gradients", implies outer works, inner lost.
    # This usually happens if the outer gradient calculation strips ANSI or overwrites it.

    outer_lines = gradient_frame(
        inner_lines,
        start_color="blue",
        end_color="cyan",
        border="rounded",
        title="Outer",
        target="border",  # If target is border, content (inner frame) should be preserved?
        # If target is both, outer gradient might tint inner?
        # The user said "NESTED GRADIENT ARCHITECTURE (Native Implementation)"
    )

    print("\n".join(outer_lines))


if __name__ == "__main__":
    main()
