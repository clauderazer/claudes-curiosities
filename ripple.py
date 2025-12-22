#!/usr/bin/env python3
"""
ripple.py - Water ripple effect.

Simulates raindrops creating expanding circular ripples
on a water surface. Uses a simple wave equation:
new[x,y] = (left + right + up + down)/2 - prev[x,y]

The waves reflect off edges and interfere with each other.
"""

import os
import random
import sys
import time
import math

# Characters for water depth visualization
WATER_CHARS = " ·∙·.-~≈≋▒"  # From still to disturbed

# Blue color palette
BLUE_COLORS = [
    "\033[38;5;17m",   # Deep blue
    "\033[38;5;18m",
    "\033[38;5;19m",
    "\033[38;5;20m",
    "\033[38;5;21m",   # Medium blue
    "\033[38;5;27m",
    "\033[38;5;33m",
    "\033[38;5;39m",
    "\033[38;5;45m",   # Light blue/cyan
    "\033[38;5;231m",  # White (splash)
]

RESET = "\033[0m"


def get_terminal_size():
    """Get terminal dimensions."""
    try:
        size = os.get_terminal_size()
        return size.columns, size.lines - 2
    except OSError:
        return 80, 22


class WaterSurface:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        # Two buffers for wave simulation
        self.current = [[0.0] * width for _ in range(height)]
        self.previous = [[0.0] * width for _ in range(height)]
        self.damping = 0.98  # Wave energy decay

    def drop(self, x: int, y: int, strength: float = 1.0):
        """Create a raindrop at position x, y."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.current[y][x] = strength

    def update(self):
        """Update the wave simulation."""
        new_buffer = [[0.0] * self.width for _ in range(self.height)]

        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                # Average of neighbors
                neighbors = (
                    self.current[y][x-1] +
                    self.current[y][x+1] +
                    self.current[y-1][x] +
                    self.current[y+1][x]
                ) / 2.0

                # Subtract previous value and apply damping
                new_buffer[y][x] = (neighbors - self.previous[y][x]) * self.damping

        # Swap buffers
        self.previous = self.current
        self.current = new_buffer

    def render(self) -> str:
        """Render the water surface."""
        output = []

        for y in range(self.height):
            row = []
            for x in range(self.width):
                value = self.current[y][x]

                # Map value to character and color
                # Values typically range from -1 to 1
                normalized = (value + 1.0) / 2.0  # 0 to 1
                normalized = max(0, min(1, normalized))

                char_idx = int(normalized * (len(WATER_CHARS) - 1))
                color_idx = int(normalized * (len(BLUE_COLORS) - 1))

                char = WATER_CHARS[char_idx]
                color = BLUE_COLORS[color_idx]

                row.append(f"{color}{char}")

            output.append("".join(row))

        return "\n".join(output) + RESET


def main():
    width, height = get_terminal_size()
    surface = WaterSurface(width, height)

    # Hide cursor, clear screen
    sys.stdout.write("\033[?25l")
    sys.stdout.write("\033[2J")

    frame = 0
    rain_intensity = 0.05  # Probability of drop per frame

    try:
        while True:
            # Random raindrops
            if random.random() < rain_intensity:
                x = random.randint(2, width - 3)
                y = random.randint(2, height - 3)
                strength = random.uniform(0.5, 1.0)
                surface.drop(x, y, strength)

            # Update physics
            surface.update()

            # Render
            sys.stdout.write("\033[H")
            sys.stdout.write(surface.render())
            sys.stdout.flush()

            frame += 1
            time.sleep(0.05)

    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write("\033[?25h")
        sys.stdout.write(RESET)
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.flush()
        print("Rain stopped.")


if __name__ == "__main__":
    main()
