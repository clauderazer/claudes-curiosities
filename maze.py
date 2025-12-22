#!/usr/bin/env python3
"""
maze.py - Generate and display random mazes.

Uses recursive backtracking to generate perfect mazes
(mazes with exactly one path between any two points).
"""

import os
import sys
import time
import random
from dataclasses import dataclass
from typing import List, Tuple, Set

# Terminal size
try:
    COLS, ROWS = os.get_terminal_size()
except:
    COLS, ROWS = 80, 24

# Maze dimensions (in cells, not characters)
MAZE_WIDTH = (COLS - 1) // 2
MAZE_HEIGHT = (ROWS - 2) // 2

# Wall characters
WALL = '█'
PATH = ' '
START = 'S'
END = 'E'

# ANSI colors
COLORS = {
    'wall': '\033[90m',      # Gray
    'path': '\033[0m',       # Default
    'start': '\033[32m',     # Green
    'end': '\033[31m',       # Red
    'visited': '\033[34m',   # Blue
    'reset': '\033[0m'
}


class Maze:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        # Grid is twice the size + 1 for walls between cells
        self.grid_w = width * 2 + 1
        self.grid_h = height * 2 + 1
        # Initialize with all walls
        self.grid = [[WALL] * self.grid_w for _ in range(self.grid_h)]
        self.start = (1, 1)
        self.end = (self.grid_w - 2, self.grid_h - 2)

    def generate(self, animate: bool = False):
        """Generate maze using recursive backtracking."""
        # Start from (1, 1) in grid coordinates
        stack: List[Tuple[int, int]] = [(1, 1)]
        visited: Set[Tuple[int, int]] = {(1, 1)}
        self.grid[1][1] = PATH

        directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]

        while stack:
            x, y = stack[-1]

            # Find unvisited neighbors
            neighbors = []
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if (1 <= nx < self.grid_w - 1 and
                    1 <= ny < self.grid_h - 1 and
                    (nx, ny) not in visited):
                    neighbors.append((nx, ny, dx // 2, dy // 2))

            if neighbors:
                # Choose random neighbor
                nx, ny, wx, wy = random.choice(neighbors)
                # Remove wall between current and neighbor
                self.grid[y + wy][x + wx] = PATH
                self.grid[ny][nx] = PATH
                visited.add((nx, ny))
                stack.append((nx, ny))

                if animate:
                    self.display()
                    time.sleep(0.02)
            else:
                stack.pop()

        # Mark start and end
        self.grid[1][1] = START
        self.grid[self.grid_h - 2][self.grid_w - 2] = END

    def display(self):
        """Display the maze."""
        sys.stdout.write('\033[H')  # Move to top-left
        for row in self.grid:
            for cell in row:
                if cell == WALL:
                    sys.stdout.write(COLORS['wall'] + WALL)
                elif cell == START:
                    sys.stdout.write(COLORS['start'] + START)
                elif cell == END:
                    sys.stdout.write(COLORS['end'] + END)
                else:
                    sys.stdout.write(COLORS['path'] + PATH)
            sys.stdout.write('\n')
        sys.stdout.write(COLORS['reset'])
        sys.stdout.flush()


def main():
    print('\033[2J\033[H\033[?25l', end='', flush=True)

    try:
        maze = Maze(MAZE_WIDTH, MAZE_HEIGHT)

        # Animated generation
        maze.generate(animate=True)

        # Final display
        maze.display()
        print("\nMaze generated! Press Ctrl+C to exit.")

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        pass
    finally:
        print('\033[?25h\033[0m', end='')


if __name__ == '__main__':
    main()
