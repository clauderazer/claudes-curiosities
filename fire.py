#!/usr/bin/env python3
"""
fire.py - Classic demoscene fire effect.

The algorithm:
1. Set the bottom row to hot values (random)
2. For each cell, average its neighbors below + small random cooling
3. Heat propagates upward, cooling as it rises
4. Map heat values to a color palette

This effect was everywhere in the 90s demoscene.
"""

import os
import random
import sys
import time

# Fire color palette (dark to bright)
FIRE_CHARS = " .:;+*oO#@"

# ANSI colors for fire gradient (232-255 grayscale + reds/oranges/yellows)
FIRE_COLORS = [
    "\033[38;5;232m",  # black
    "\033[38;5;52m",   # dark red
    "\033[38;5;88m",   # darker red
    "\033[38;5;124m",  # dark red
    "\033[38;5;160m",  # red
    "\033[38;5;196m",  # bright red
    "\033[38;5;202m",  # orange-red
    "\033[38;5;208m",  # orange
    "\033[38;5;214m",  # light orange
    "\033[38;5;220m",  # yellow-orange
    "\033[38;5;226m",  # yellow
    "\033[38;5;227m",  # light yellow
    "\033[38;5;228m",  # pale yellow
    "\033[38;5;229m",  # very pale yellow
    "\033[38;5;230m",  # almost white
    "\033[38;5;231m",  # white
]

RESET = "\033[0m"


def get_terminal_size():
    """Get terminal dimensions."""
    try:
        size = os.get_terminal_size()
        return size.columns, size.lines
    except OSError:
        return 80, 24


class Fire:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        # Heat buffer - values from 0 to 255
        self.buffer = [[0] * width for _ in range(height)]

    def spark(self):
        """Create hot spots at the bottom."""
        for x in range(self.width):
            # Random intensity at bottom
            if random.random() < 0.7:
                self.buffer[self.height - 1][x] = random.randint(180, 255)
            else:
                self.buffer[self.height - 1][x] = random.randint(100, 200)

    def propagate(self):
        """Propagate heat upward with cooling."""
        new_buffer = [[0] * self.width for _ in range(self.height)]

        for y in range(self.height - 1):  # Don't process bottom row
            for x in range(self.width):
                # Sample from cells below
                samples = []

                # Below
                if y + 1 < self.height:
                    samples.append(self.buffer[y + 1][x])
                    # Below-left
                    if x > 0:
                        samples.append(self.buffer[y + 1][x - 1])
                    # Below-right
                    if x < self.width - 1:
                        samples.append(self.buffer[y + 1][x + 1])

                # Sometimes sample two below
                if y + 2 < self.height:
                    samples.append(self.buffer[y + 2][x])

                if samples:
                    # Average with slight cooling
                    avg = sum(samples) / len(samples)
                    # Cooling factor - more cooling = shorter flames
                    cooling = random.uniform(0.8, 1.2)
                    new_val = avg - cooling * 3
                    new_buffer[y][x] = max(0, min(255, int(new_val)))

        self.buffer = new_buffer

    def render(self) -> str:
        """Render the fire to a string."""
        output = []

        for y in range(self.height):
            row = []
            for x in range(self.width):
                heat = self.buffer[y][x]

                # Map heat to color and character
                color_idx = min(len(FIRE_COLORS) - 1, heat * len(FIRE_COLORS) // 256)
                char_idx = min(len(FIRE_CHARS) - 1, heat * len(FIRE_CHARS) // 256)

                color = FIRE_COLORS[color_idx]
                char = FIRE_CHARS[char_idx]

                row.append(f"{color}{char}")

            output.append("".join(row))

        return "\n".join(output) + RESET


def main():
    # Get terminal size and leave room for status
    width, height = get_terminal_size()
    height = height - 2

    fire = Fire(width, height)

    # Hide cursor, clear screen
    sys.stdout.write("\033[?25l")  # Hide cursor
    sys.stdout.write("\033[2J")    # Clear screen

    try:
        frame = 0
        while True:
            # Create sparks at bottom
            fire.spark()

            # Propagate heat upward
            fire.propagate()

            # Render
            sys.stdout.write("\033[H")  # Move to top-left
            sys.stdout.write(fire.render())
            sys.stdout.flush()

            frame += 1
            time.sleep(0.03)

    except KeyboardInterrupt:
        pass
    finally:
        # Show cursor, reset colors
        sys.stdout.write("\033[?25h")
        sys.stdout.write(RESET)
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.flush()
        print("Fire extinguished.")


if __name__ == "__main__":
    main()
