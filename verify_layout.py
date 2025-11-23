from styledconsole import Console


def verify_fix():
    console = Console()
    print("--- Testing MASTERPIECE Banner (Should not wrap and be centered) ---")
    console.banner("MASTERPIECE", font="banner", start_color="red", end_color="violet")
    print("\n--- Testing Centered Frame ---")
    console.frame("This frame should be centered", align="center", width=40)


if __name__ == "__main__":
    verify_fix()
