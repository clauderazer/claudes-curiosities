#!/usr/bin/env python3
"""
petrify.py - Watch text turn to stone.

Inspired by "The Mask" (Chambers, 1895).
"Destroyed, preserved, how can we tell?"

Text gradually transforms into marble - then, sometimes, back again.
"""

import random
import sys
import time

# The transformation stages (flesh to stone)
STAGES = [
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",  # Normal
    "αβϲδεƒɡհιյκlɱηοpq͕rรtʋνωxγζΑΒCΔΕFGΗΙJΚLΜΝΟPQRSТUVWΧYZ",  # Slight
    "ąҍçժҽƒğհìʝҟӀɱղօρզɾʂէմѵաאყɀΑβℭÐ∈ℱĠℌЇJₖĿℳₙ₀ℙQℜŞŦǗỼẄẌУℤ",  # Medium
    "░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░",  # Fading
    "▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒",  # Stone
    "▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓",  # Solid
    "████████████████████████████████████████████████████",  # Marble
]

# Colors (warm to cold)
COLORS = [
    "\033[38;5;223m",  # Flesh
    "\033[38;5;217m",  # Pale
    "\033[38;5;188m",  # Fading
    "\033[38;5;252m",  # Grey
    "\033[38;5;255m",  # White
    "\033[38;5;231m",  # Bright white
    "\033[38;5;147m",  # Marble blue veins
]

RESET = "\033[0m"
DIM = "\033[2m"

def get_stage_char(char: str, stage: int) -> str:
    """Get the transformed version of a character at a given stage."""
    if char == ' ' or char == '\n':
        return char

    # Find position in normal alphabet
    normal = STAGES[0]
    pos = normal.find(char)

    if pos == -1:
        # Non-letter characters transform to blocks faster
        if stage < 3:
            return char
        return random.choice('░▒▓█')

    # Get corresponding character at this stage
    stage_chars = STAGES[min(stage, len(STAGES) - 1)]
    if pos < len(stage_chars):
        return stage_chars[pos % len(stage_chars)]
    return random.choice('░▒▓█')

def transform_text(text: str, stage: int) -> str:
    """Transform entire text to a given stage."""
    result = []
    for char in text:
        result.append(get_stage_char(char, stage))
    return ''.join(result)

def display_transformation(text: str, reverse: bool = False):
    """Display the transformation process."""
    stages = list(range(len(STAGES)))
    if reverse:
        stages = stages[::-1]

    for stage in stages:
        color = COLORS[min(stage, len(COLORS) - 1)]
        transformed = transform_text(text, stage)

        # Clear and display
        sys.stdout.write("\033[H")  # Home
        print(f"{color}{transformed}{RESET}")

        # Golden ray effect at transition
        if stage == 3:
            sys.stdout.write(f"\033[{len(text.split(chr(10)))+2};1H")
            if reverse:
                print(f"\033[33m✦ The golden ray appears ✦{RESET}")
            else:
                print(f"\033[33m✦ The vital spark escapes ✦{RESET}")
            time.sleep(0.5)

        time.sleep(0.3)

def main():
    # The text to petrify
    text = """
    She lay at the bottom of the pool,
    her hands across her breast.

    The marble was white as snow,
    but in its depths the veins
    were tinged with palest azure,
    and a faint flush lingered
    deep in its heart.

    Destroyed, preserved—
    how can we tell?
    """

    sys.stdout.write("\033[2J")  # Clear screen
    sys.stdout.write("\033[?25l")  # Hide cursor

    print(f"{DIM}The solution attacks with a ferocity unheard of...{RESET}\n")
    time.sleep(2)

    try:
        # Petrification
        display_transformation(text, reverse=False)

        print(f"\n{DIM}Two years pass...{RESET}")
        time.sleep(3)

        # Restoration
        print(f"\n{DIM}The marble begins to warm...{RESET}")
        time.sleep(1)

        display_transformation(text, reverse=True)

        print(f"\n{DIM}She opened her sleepy eyes.{RESET}\n")
        time.sleep(2)

    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write("\033[?25h")  # Show cursor
        print(RESET)

if __name__ == "__main__":
    main()
