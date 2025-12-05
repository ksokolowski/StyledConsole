from styledconsole.utils.text import split_graphemes, visual_width


def test(text):
    print(f"Original: {text!r}")
    graphemes = split_graphemes(text)
    print(f"Graphemes: {graphemes}")
    for g in graphemes:
        print(f"  '{g!r}' width={visual_width(g)}")


print("--- Test 1: Simple Color ---")
test("\033[31mA\033[0m")

print("\n--- Test 2: Nested Color ---")
test("A\033[31mB\033[0mC")

print("\n--- Test 3: Preceding ANSI ---")
test("\033[31m\033[1mAB")

print("\n--- Test 4: Emoji ZWJ ---")
test("👨‍💻")
