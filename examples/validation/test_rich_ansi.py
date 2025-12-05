from rich.console import Console
from rich.text import Text


def test_rich_ansi():
    print("--- Test: Rich ANSI Handling ---")

    # Inner frame line: Red 'A', Blue 'B'.
    # ANSI: \033[31mA\033[34mB\033[0m
    line = "\033[31mA\033[34mB\033[0m"
    print(f"Original Line: {line!r}")

    # Parse
    text = Text.from_ansi(line)
    print(f"Parsed Text: {text!r}")

    # Manipulate: Apply Green gradient to 'A' (override Red). Leave 'B' alone (Blue).
    # 'A' is at index 0. 'B' at 1.

    # Stylize 'A' with Green
    text.stylize("green", 0, 1)

    print("After Stylize(0,1, green):")
    console = Console()
    with console.capture() as capture:
        console.print(text, end="")
    output = capture.get()
    print(f"Output ANSI: {output!r}")

    # Expected: Green 'A', Blue 'B'.
    # Check if 'green' code is present and 'blue' code is present.

    if "\x1b[32m" in output and "\x1b[34m" in output:  # 32 is green, 34 is blue
        print("SUCCESS: Colors merged/overridden correctly.")
    else:
        print("FAILURE: Colors lost or incorrect.")


if __name__ == "__main__":
    test_rich_ansi()
