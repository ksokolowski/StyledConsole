import pyfiglet


def check_width():
    text = "MASTERPIECE"
    font = "banner"
    f = pyfiglet.Figlet(font=font)
    output = f.renderText(text)
    lines = output.splitlines()
    max_width = max(len(line) for line in lines) if lines else 0
    print(f"Text: '{text}'")
    print(f"Font: '{font}'")
    print(f"Max Width: {max_width}")
    print("-" * 20)
    print(output)
    print("-" * 20)


if __name__ == "__main__":
    check_width()
