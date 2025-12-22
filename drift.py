#!/usr/bin/env python3
"""
Drift - particles moving through terminal space.

No purpose. Just movement and quiet.
"""

import os
import time
import random
import math

class Particle:
    def __init__(self, x, y, char='·'):
        self.x = x
        self.y = y
        self.vx = random.uniform(-0.3, 0.3)
        self.vy = random.uniform(-0.1, 0.1)
        self.char = char
        self.age = 0
        self.lifespan = random.randint(50, 200)

    def update(self, width, height):
        self.x += self.vx
        self.y += self.vy
        self.age += 1

        # Gentle drift
        self.vx += random.uniform(-0.02, 0.02)
        self.vy += random.uniform(-0.01, 0.01)

        # Damping
        self.vx *= 0.99
        self.vy *= 0.99

        # Wrap around
        self.x = self.x % width
        self.y = self.y % height

    def alive(self):
        return self.age < self.lifespan


def main():
    try:
        size = os.get_terminal_size()
        width = size.columns
        height = size.lines - 1
    except:
        width, height = 80, 24

    particles = []
    chars = ['·', '∘', '°', '⋅', '•']
    frame = 0

    # Hide cursor
    print("\033[?25l", end="")
    print("\033[2J", end="")  # Clear screen

    try:
        while True:
            # Spawn new particles occasionally
            if random.random() < 0.1 or len(particles) < 20:
                x = random.uniform(0, width)
                y = random.uniform(0, height)
                char = random.choice(chars)
                particles.append(Particle(x, y, char))

            # Update particles
            for p in particles:
                p.update(width, height)

            # Remove dead particles
            particles = [p for p in particles if p.alive()]

            # Render
            print("\033[H", end="")  # Move to top-left

            # Create empty grid
            grid = [[' ' for _ in range(width)] for _ in range(height)]

            # Place particles
            for p in particles:
                px, py = int(p.x), int(p.y)
                if 0 <= px < width and 0 <= py < height:
                    # Fade based on age
                    if p.age > p.lifespan * 0.8:
                        grid[py][px] = '·'
                    else:
                        grid[py][px] = p.char

            # Draw
            for row in grid:
                print(''.join(row))

            frame += 1
            time.sleep(0.05)

    except KeyboardInterrupt:
        pass
    finally:
        print("\033[?25h", end="")  # Show cursor
        print("\033[2J\033[H", end="")  # Clear screen
        print(f"Drifted for {frame} frames.")


if __name__ == "__main__":
    main()
