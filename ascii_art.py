#!/usr/bin/env python3
"""
Simple ASCII art generator - converts text to block letters
"""

LETTERS = {
    'A': [
        "  █  ",
        " █ █ ",
        "█████",
        "█   █",
        "█   █"
    ],
    'B': [
        "████ ",
        "█   █",
        "████ ",
        "█   █",
        "████ "
    ],
    'C': [
        " ████",
        "█    ",
        "█    ",
        "█    ",
        " ████"
    ],
    'D': [
        "████ ",
        "█   █",
        "█   █",
        "█   █",
        "████ "
    ],
    'E': [
        "█████",
        "█    ",
        "███  ",
        "█    ",
        "█████"
    ],
    'F': [
        "█████",
        "█    ",
        "███  ",
        "█    ",
        "█    "
    ],
    'G': [
        " ████",
        "█    ",
        "█  ██",
        "█   █",
        " ████"
    ],
    'H': [
        "█   █",
        "█   █",
        "█████",
        "█   █",
        "█   █"
    ],
    'I': [
        "█████",
        "  █  ",
        "  █  ",
        "  █  ",
        "█████"
    ],
    'J': [
        "█████",
        "   █ ",
        "   █ ",
        "█  █ ",
        " ██  "
    ],
    'K': [
        "█   █",
        "█  █ ",
        "███  ",
        "█  █ ",
        "█   █"
    ],
    'L': [
        "█    ",
        "█    ",
        "█    ",
        "█    ",
        "█████"
    ],
    'M': [
        "█   █",
        "██ ██",
        "█ █ █",
        "█   █",
        "█   █"
    ],
    'N': [
        "█   █",
        "██  █",
        "█ █ █",
        "█  ██",
        "█   █"
    ],
    'O': [
        " ███ ",
        "█   █",
        "█   █",
        "█   █",
        " ███ "
    ],
    'P': [
        "████ ",
        "█   █",
        "████ ",
        "█    ",
        "█    "
    ],
    'Q': [
        " ███ ",
        "█   █",
        "█   █",
        "█  █ ",
        " ██ █"
    ],
    'R': [
        "████ ",
        "█   █",
        "████ ",
        "█  █ ",
        "█   █"
    ],
    'S': [
        " ████",
        "█    ",
        " ███ ",
        "    █",
        "████ "
    ],
    'T': [
        "█████",
        "  █  ",
        "  █  ",
        "  █  ",
        "  █  "
    ],
    'U': [
        "█   █",
        "█   █",
        "█   █",
        "█   █",
        " ███ "
    ],
    'V': [
        "█   █",
        "█   █",
        "█   █",
        " █ █ ",
        "  █  "
    ],
    'W': [
        "█   █",
        "█   █",
        "█ █ █",
        "██ ██",
        "█   █"
    ],
    'X': [
        "█   █",
        " █ █ ",
        "  █  ",
        " █ █ ",
        "█   █"
    ],
    'Y': [
        "█   █",
        " █ █ ",
        "  █  ",
        "  █  ",
        "  █  "
    ],
    'Z': [
        "█████",
        "   █ ",
        "  █  ",
        " █   ",
        "█████"
    ],
    ' ': [
        "     ",
        "     ",
        "     ",
        "     ",
        "     "
    ],
    '!': [
        "  █  ",
        "  █  ",
        "  █  ",
        "     ",
        "  █  "
    ],
    '?': [
        " ███ ",
        "█   █",
        "  █  ",
        "     ",
        "  █  "
    ],
}

def text_to_ascii(text):
    """Convert text to ASCII block letters"""
    text = text.upper()
    lines = ["", "", "", "", ""]

    for char in text:
        if char in LETTERS:
            for i, row in enumerate(LETTERS[char]):
                lines[i] += row + " "
        else:
            # Unknown character - use space
            for i in range(5):
                lines[i] += "      "

    return "\n".join(lines)

def banner(text, border_char="═"):
    """Create a banner with the text"""
    ascii_text = text_to_ascii(text)
    width = max(len(line) for line in ascii_text.split("\n")) + 4

    top = "╔" + border_char * width + "╗"
    bottom = "╚" + border_char * width + "╝"

    result = [top]
    for line in ascii_text.split("\n"):
        padded = line + " " * (width - len(line))
        result.append("║ " + padded + " ║")
    result.append(bottom)

    return "\n".join(result)

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
    else:
        text = "HELLO"

    print(banner(text))
    print()
    print("Plain:")
    print(text_to_ascii(text))
