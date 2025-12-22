#!/usr/bin/env python3
"""
plasma.py - A demoscene-inspired plasma effect in the terminal.

Classic plasma uses overlapping sine waves to create organic, flowing patterns.
This is the kind of effect you'd see in 90s demos like Second Reality.
"""

import os
import sys
import time
import math

# Terminal size
try:
    COLS, ROWS = os.get_terminal_size()
except:
    COLS, ROWS = 80, 24

ROWS -= 1

# Characters for intensity levels (dark to bright)
CHARS = ' ·.,:;+*#@'

# Color palettes using ANSI colors
PALETTE = [
    '\033[38;5;16m',   # black
    '\033[38;5;17m',   # dark blue
    '\033[38;5;18m',   # blue
    '\033[38;5;19m',   # blue
    '\033[38;5;20m',   # brighter blue
    '\033[38;5;21m',   # bright blue
    '\033[38;5;57m',   # purple
    '\033[38;5;93m',   # violet
    '\033[38;5;129m',  # magenta
    '\033[38;5;165m',  # pink
    '\033[38;5;201m',  # bright pink
    '\033[38;5;207m',  # light pink
    '\033[38;5;213m',  # pale pink
    '\033[38;5;219m',  # very light pink
    '\033[38;5;225m',  # almost white
    '\033[38;5;231m',  # white
]

RESET = '\033[0m'

def plasma(x: float, y: float, t: float) -> float:
    """
    Classic plasma function using overlapping sine waves.
    Returns a value between 0 and 1.
    """
    # Scale coordinates
    x = x * 0.1
    y = y * 0.1

    # Multiple sine waves at different frequencies and phases
    v = 0.0

    # Horizontal wave
    v += math.sin(x + t)

    # Vertical wave
    v += math.sin(y + t * 0.7)

    # Diagonal wave
    v += math.sin((x + y + t) * 0.5)

    # Circular wave
    cx = x + 0.5 * math.sin(t * 0.3)
    cy = y + 0.5 * math.cos(t * 0.4)
    v += math.sin(math.sqrt(cx*cx + cy*cy + 1) + t)

    # Another circular wave offset
    cx2 = x + 0.3 * math.cos(t * 0.5)
    cy2 = y + 0.3 * math.sin(t * 0.6)
    v += math.sin(math.sqrt(cx2*cx2 + cy2*cy2 + 1) * 2 - t * 0.8)

    # Normalize to 0-1
    return (v + 5) / 10

def run():
    """Main loop."""
    # Hide cursor, clear screen
    print('\033[?25l\033[2J', end='', flush=True)

    t = 0.0
    dt = 0.08

    try:
        while True:
            start = time.time()

            # Build frame
            frame = '\033[H'  # Move to top-left

            for y in range(ROWS):
                for x in range(COLS):
                    # Get plasma value
                    v = plasma(x, y, t)

                    # Map to palette
                    idx = int(v * (len(PALETTE) - 1))
                    idx = max(0, min(len(PALETTE) - 1, idx))

                    # Map to character
                    char_idx = int(v * (len(CHARS) - 1))
                    char_idx = max(0, min(len(CHARS) - 1, char_idx))

                    frame += PALETTE[idx] + CHARS[char_idx]

                if y < ROWS - 1:
                    frame += '\n'

            frame += RESET

            sys.stdout.write(frame)
            sys.stdout.flush()

            t += dt

            # Timing
            elapsed = time.time() - start
            if elapsed < dt:
                time.sleep(dt - elapsed)

    except KeyboardInterrupt:
        pass
    finally:
        # Show cursor, reset colors, clear
        print('\033[?25h\033[0m\033[2J\033[H', end='')

if __name__ == '__main__':
    print("plasma.py - Classic demoscene effect")
    print("Press Ctrl+C to exit")
    time.sleep(1)
    run()
