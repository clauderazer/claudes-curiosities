#!/usr/bin/env python3
"""
ant.py - Langton's Ant

A two-dimensional universal Turing machine with simple rules:
1. On a white square: turn 90° right, flip color, move forward
2. On a black square: turn 90° left, flip color, move forward

After about 10,000 steps of seeming chaos, the ant spontaneously
starts building an infinite diagonal "highway" pattern.

This emergence from simple rules is one of the beautiful mysteries
of cellular automata.
"""

import os
import sys
import time

# Direction vectors: N, E, S, W
DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]
DIRECTION_CHARS = ['▲', '►', '▼', '◄']

# Colors
WHITE = "\033[48;5;231m \033[0m"  # White background
BLACK = "\033[48;5;232m \033[0m"  # Black background
ANT_WHITE = "\033[48;5;231m\033[38;5;196m"  # Ant on white
ANT_BLACK = "\033[48;5;232m\033[38;5;196m"  # Ant on black
RESET = "\033[0m"


def get_terminal_size():
    """Get terminal dimensions."""
    try:
        size = os.get_terminal_size()
        return size.columns, size.lines - 2
    except OSError:
        return 80, 22


class LangtonAnt:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        # Grid: False = white, True = black
        self.grid = [[False] * width for _ in range(height)]
        # Ant position and direction (0=N, 1=E, 2=S, 3=W)
        self.ant_x = width // 2
        self.ant_y = height // 2
        self.direction = 0  # North
        self.steps = 0

    def step(self):
        """Execute one step of the ant."""
        x, y = self.ant_x, self.ant_y

        # Get current cell color
        is_black = self.grid[y][x]

        if is_black:
            # On black: turn left
            self.direction = (self.direction - 1) % 4
        else:
            # On white: turn right
            self.direction = (self.direction + 1) % 4

        # Flip the color
        self.grid[y][x] = not is_black

        # Move forward
        dx, dy = DIRECTIONS[self.direction]
        self.ant_x = (x + dx) % self.width
        self.ant_y = (y + dy) % self.height

        self.steps += 1

    def render(self) -> str:
        """Render the grid with the ant."""
        output = []

        for y in range(self.height):
            row = []
            for x in range(self.width):
                if x == self.ant_x and y == self.ant_y:
                    # Draw ant
                    is_black = self.grid[y][x]
                    if is_black:
                        row.append(f"{ANT_BLACK}{DIRECTION_CHARS[self.direction]}{RESET}")
                    else:
                        row.append(f"{ANT_WHITE}{DIRECTION_CHARS[self.direction]}{RESET}")
                else:
                    # Draw cell
                    if self.grid[y][x]:
                        row.append(BLACK)
                    else:
                        row.append(WHITE)
            output.append("".join(row))

        return "\n".join(output)


def main():
    width, height = get_terminal_size()

    ant = LangtonAnt(width, height)

    # Hide cursor, clear screen
    sys.stdout.write("\033[?25l")
    sys.stdout.write("\033[2J")

    # Steps per frame (increase for faster simulation)
    steps_per_frame = 10

    try:
        while True:
            # Run multiple steps per frame for speed
            for _ in range(steps_per_frame):
                ant.step()

            # Render
            sys.stdout.write("\033[H")
            sys.stdout.write(ant.render())
            sys.stdout.write(f"\n\033[K Step: {ant.steps:,}")
            sys.stdout.flush()

            # Adaptive speed - faster after highway starts
            if ant.steps > 10000:
                steps_per_frame = 50
            if ant.steps > 50000:
                steps_per_frame = 100

            time.sleep(0.03)

    except KeyboardInterrupt:
        pass
    finally:
        # Show cursor, reset
        sys.stdout.write("\033[?25h")
        sys.stdout.write(RESET)
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.flush()
        print(f"Langton's Ant: {ant.steps:,} steps")


if __name__ == "__main__":
    main()
