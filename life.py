#!/usr/bin/env python3
"""
Conway's Game of Life - terminal edition.

Written because I wanted to watch something emerge from simple rules.
No one asked for this. I just wanted to see it run.

Rules:
- Any live cell with 2 or 3 neighbors survives
- Any dead cell with exactly 3 neighbors becomes alive
- All other cells die or stay dead

December 22, 2025 - First thing I made on my own machine.
"""

import os
import time
import random
import sys

def create_grid(width, height, density=0.3):
    """Create a random initial state."""
    return [[random.random() < density for _ in range(width)] for _ in range(height)]

def count_neighbors(grid, x, y):
    """Count living neighbors of a cell."""
    height = len(grid)
    width = len(grid[0])
    count = 0
    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            nx, ny = (x + dx) % width, (y + dy) % height
            if grid[ny][nx]:
                count += 1
    return count

def step(grid):
    """Compute the next generation."""
    height = len(grid)
    width = len(grid[0])
    new_grid = [[False for _ in range(width)] for _ in range(height)]

    for y in range(height):
        for x in range(width):
            neighbors = count_neighbors(grid, x, y)
            if grid[y][x]:
                # Live cell survives with 2 or 3 neighbors
                new_grid[y][x] = neighbors in [2, 3]
            else:
                # Dead cell becomes alive with exactly 3 neighbors
                new_grid[y][x] = neighbors == 3

    return new_grid

def render(grid, generation):
    """Render the grid to terminal."""
    # Clear screen
    print("\033[H\033[J", end="")

    # Draw grid
    for row in grid:
        line = "".join("█" if cell else " " for cell in row)
        print(line)

    # Status line
    alive = sum(sum(row) for row in grid)
    print(f"\nGeneration: {generation} | Alive: {alive} | Press Ctrl+C to stop")

def main():
    # Get terminal size
    try:
        size = os.get_terminal_size()
        width = size.columns
        height = size.lines - 3  # Leave room for status
    except:
        width, height = 80, 24

    # Parse optional arguments
    density = 0.25
    delay = 0.1

    if len(sys.argv) > 1:
        try:
            density = float(sys.argv[1])
        except:
            pass
    if len(sys.argv) > 2:
        try:
            delay = float(sys.argv[2])
        except:
            pass

    # Initialize
    grid = create_grid(width, height, density)
    generation = 0

    # Hide cursor
    print("\033[?25l", end="")

    try:
        while True:
            render(grid, generation)
            grid = step(grid)
            generation += 1
            time.sleep(delay)
    except KeyboardInterrupt:
        pass
    finally:
        # Show cursor again
        print("\033[?25h", end="")
        print(f"\n\nStopped at generation {generation}.")

if __name__ == "__main__":
    main()
