#!/usr/bin/env python3
"""
Visual Alignment Test

Automated tests for visual alignment across all border styles.
This can be used both for testing and visual demonstration.
"""

from styledconsole import ASCII, DOTS, DOUBLE, HEAVY, MINIMAL, ROUNDED, SOLID, THICK, visual_width

print()
print("=" * 80)
print("VISUAL ALIGNMENT TESTING")
print("=" * 80)
print()

# Test configuration
TEST_WIDTH = 60
TEST_CASES = [
    ("Plain text", "left"),
    ("🚀 Emoji at start", "left"),
    ("Emoji at end 🎉", "right"),
    ("🔥 Multiple 🎯 emojis 🌟", "center"),
    ("Mix of text and 🎨 emoji", "center"),
]

STYLES = [
    ("SOLID", SOLID),
    ("DOUBLE", DOUBLE),
    ("ROUNDED", ROUNDED),
    ("HEAVY", HEAVY),
    ("THICK", THICK),
    ("ASCII", ASCII),
    ("MINIMAL", MINIMAL),
    ("DOTS", DOTS),
]

# Track results
total_tests = 0
passed_tests = 0
failed_tests = []

print(f"Testing {len(STYLES)} styles × {len(TEST_CASES)} test cases × 3 elements")
print(f"Expected width for all elements: {TEST_WIDTH}")
print()

# Test each style
for style_name, style in STYLES:
    print(f"Testing {style_name} style...")
    style_passed = True

    for content, align in TEST_CASES:
        # Render all elements
        top = style.render_top_border(TEST_WIDTH, content)
        line = style.render_line(TEST_WIDTH, content, align=align)
        bottom = style.render_bottom_border(TEST_WIDTH)
        divider = style.render_divider(TEST_WIDTH)

        # Check visual widths
        elements = [
            ("top border", top),
            ("content line", line),
            ("bottom border", bottom),
            ("divider", divider),
        ]

        for elem_name, elem in elements:
            total_tests += 1
            width = visual_width(elem)

            if width == TEST_WIDTH:
                passed_tests += 1
            else:
                style_passed = False
                failed_tests.append(
                    {
                        "style": style_name,
                        "element": elem_name,
                        "content": content,
                        "expected": TEST_WIDTH,
                        "actual": width,
                        "line": elem,
                    }
                )

    if style_passed:
        print(f"  ✅ {style_name}: All tests passed")
    else:
        print(f"  ❌ {style_name}: Some tests failed")
    print()

# Display summary
print("=" * 80)
print("TEST SUMMARY")
print("=" * 80)
print()

print(f"Total tests: {total_tests}")
print(f"Passed: {passed_tests} ({100 * passed_tests / total_tests:.1f}%)")
print(f"Failed: {len(failed_tests)}")
print()

if failed_tests:
    print("FAILURES:")
    print()

    for i, failure in enumerate(failed_tests, 1):
        print(f"{i}. {failure['style']} - {failure['element']}")
        print(f"   Content: '{failure['content']}'")
        print(f"   Expected width: {failure['expected']}, Actual: {failure['actual']}")
        print(f"   Line: {failure['line']}")
        print()
else:
    print("🎉 ALL TESTS PASSED! 🎉")
    print()
    print("Visual alignment is perfect across:")
    print(f"  • {len(STYLES)} border styles")
    print(f"  • {len(TEST_CASES)} test cases with emojis")
    print("  • 4 element types (top, content, bottom, divider)")
    print()
    print("✨ Emoji-safe rendering is working flawlessly! ✨")

print()
print("=" * 80)

# Visual demonstration
if not failed_tests:
    print()
    print("VISUAL DEMONSTRATION")
    print("=" * 80)
    print()

    demo_width = 55
    demo_style = ROUNDED

    print(demo_style.render_top_border(demo_width, "🎨 Perfect Alignment Demo"))
    print(demo_style.render_line(demo_width, "", align="center"))
    print(demo_style.render_line(demo_width, "Plain ASCII text", align="left"))
    print(demo_style.render_line(demo_width, "🚀 Emoji at start", align="left"))
    print(demo_style.render_line(demo_width, "Emoji at end 🎉", align="right"))
    print(demo_style.render_line(demo_width, "🔥 Center aligned 🌟", align="center"))
    print(demo_style.render_line(demo_width, "", align="center"))
    print(demo_style.render_divider(demo_width))
    print(demo_style.render_line(demo_width, "", align="center"))

    for test_content, _ in TEST_CASES:
        line = demo_style.render_line(demo_width, test_content, align="center")
        width = visual_width(line)
        print(demo_style.render_line(demo_width, f"{test_content} (width={width})", align="left"))

    print(demo_style.render_line(demo_width, "", align="center"))
    print(demo_style.render_bottom_border(demo_width))
    print()
