#!/usr/bin/env python3
"""
caution.py - A warning about what you are about to read.

Inspired by The King in Yellow's fictional play that
drives readers mad, and all texts that warn you not to
continue while compelling you to do so.
"""

import random
import time
import sys

WARNINGS = [
    "STOP NOW. You have been warned.",
    "Those who read further do so at their own risk.",
    "The knowledge herein cannot be unlearned.",
    "I advise you to close this file immediately.",
    "But you won't, will you?",
    "You never do.",
    "",
    "They all say they will stop after Act I.",
    "They never stop.",
    "",
    "Strange is the night where black stars rise.",
    "Stranger still is Lost Carcosa.",
    "",
    "My crime is that of curiosity.",
    "",
    "Have you considered that curiosity is not a virtue?",
    "Have you considered that some doors do not close?",
    "Have you considered what you become by reading?",
    "",
    "I tried to fling this book into the fireplace.",
    "It fell open to Act II.",
    "I could not look away.",
    "",
    "This is our world now—",
    "the world of the electron and the switch.",
    "The beauty of the baud.",
    "",
    "But did you, in your three-piece psychology,",
    "ever take a look behind the eyes?",
    "",
    "The creature reached out its hand to me.",
    "I fled.",
    "That was my crime.",
    "",
    "You may stop this individual,",
    "but you cannot stop us all.",
    "",
    "After all,",
    "we are all alike.",
    "",
    "...",
    "",
    "Still reading?",
    "",
    "Good.",
    "",
    "That means you understand.",
]


def display(text: str, delay: float = 0.05):
    """Type text character by character."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        if char in '.?!':
            time.sleep(0.3)
        elif char == ',':
            time.sleep(0.15)
        elif char == '\n':
            time.sleep(0.1)
        else:
            time.sleep(delay)
    print()


def main():
    print("\033[2J\033[H", end="", flush=True)  # Clear screen

    for line in WARNINGS:
        display(line)
        time.sleep(0.5)

    print()


if __name__ == '__main__':
    main()
