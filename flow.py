#!/usr/bin/env python3
"""
flow.py - A flowing particle system in the terminal.

Particles drift across the screen following a vector field,
creating trails that fade over time. Like watching ink in water.
"""

import os
import sys
import time
import math
import random
from dataclasses import dataclass
from typing import List, Tuple

# Terminal size
try:
    COLS, ROWS = os.get_terminal_size()
except:
    COLS, ROWS = 80, 24

ROWS -= 1  # Leave room for cursor

# Characters for different densities
CHARS = ' .·:+*#@'

@dataclass
class Particle:
    x: float
    y: float
    vx: float = 0.0
    vy: float = 0.0
    life: float = 1.0

class FlowField:
    """A vector field that particles follow."""

    def __init__(self, scale: float = 0.1, time_scale: float = 0.3):
        self.scale = scale
        self.time_scale = time_scale
        self.time = 0.0

    def get_vector(self, x: float, y: float) -> Tuple[float, float]:
        """Get the flow vector at a point using Perlin-like noise."""
        # Simple pseudo-noise based on sin/cos combinations
        t = self.time
        nx = x * self.scale
        ny = y * self.scale

        # Multiple octaves of sine waves for interesting patterns
        angle = (
            math.sin(nx + t) * 2 +
            math.cos(ny * 1.3 + t * 0.7) * 1.5 +
            math.sin(nx * 0.5 + ny * 0.5 + t * 1.2) +
            math.cos(nx * 2 - ny + t * 0.3) * 0.5
        )

        return math.cos(angle), math.sin(angle)

    def update(self, dt: float):
        self.time += dt * self.time_scale

class Canvas:
    """A character canvas with density tracking."""

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.density = [[0.0] * width for _ in range(height)]

    def add(self, x: float, y: float, amount: float = 1.0):
        """Add density at a point."""
        ix, iy = int(x), int(y)
        if 0 <= ix < self.width and 0 <= iy < self.height:
            self.density[iy][ix] += amount

    def fade(self, factor: float = 0.95):
        """Fade all density values."""
        for y in range(self.height):
            for x in range(self.width):
                self.density[y][x] *= factor

    def render(self) -> str:
        """Render the canvas to a string."""
        lines = []
        for row in self.density:
            line = ''
            for d in row:
                idx = min(int(d * 2), len(CHARS) - 1)
                line += CHARS[idx]
            lines.append(line)
        return '\n'.join(lines)

def spawn_particle(width: int, height: int) -> Particle:
    """Spawn a particle at a random edge or center."""
    if random.random() < 0.3:
        # Center spawn
        return Particle(
            x=width/2 + random.gauss(0, width/6),
            y=height/2 + random.gauss(0, height/6)
        )
    else:
        # Edge spawn
        edge = random.randint(0, 3)
        if edge == 0:  # Top
            return Particle(x=random.random() * width, y=0)
        elif edge == 1:  # Bottom
            return Particle(x=random.random() * width, y=height-1)
        elif edge == 2:  # Left
            return Particle(x=0, y=random.random() * height)
        else:  # Right
            return Particle(x=width-1, y=random.random() * height)

def run():
    """Main loop."""
    # Hide cursor
    print('\033[?25l', end='', flush=True)

    try:
        field = FlowField(scale=0.15, time_scale=0.5)
        canvas = Canvas(COLS, ROWS)
        particles: List[Particle] = []

        max_particles = 200
        spawn_rate = 5

        dt = 0.05

        while True:
            start = time.time()

            # Spawn new particles
            for _ in range(spawn_rate):
                if len(particles) < max_particles:
                    particles.append(spawn_particle(COLS, ROWS))

            # Update particles
            new_particles = []
            for p in particles:
                # Get flow vector
                fx, fy = field.get_vector(p.x, p.y)

                # Update velocity with flow and some randomness
                p.vx = p.vx * 0.9 + fx * 0.5 + random.gauss(0, 0.1)
                p.vy = p.vy * 0.9 + fy * 0.5 + random.gauss(0, 0.1)

                # Update position
                p.x += p.vx
                p.y += p.vy

                # Age particle
                p.life -= 0.005

                # Add to canvas
                canvas.add(p.x, p.y, p.life * 0.8)

                # Keep if still alive and in bounds
                if (p.life > 0 and
                    0 <= p.x < COLS and
                    0 <= p.y < ROWS):
                    new_particles.append(p)

            particles = new_particles

            # Fade canvas
            canvas.fade(0.92)

            # Update field
            field.update(dt)

            # Render
            sys.stdout.write('\033[H')  # Move to top-left
            sys.stdout.write(canvas.render())
            sys.stdout.flush()

            # Timing
            elapsed = time.time() - start
            if elapsed < dt:
                time.sleep(dt - elapsed)

    except KeyboardInterrupt:
        pass
    finally:
        # Show cursor and clear
        print('\033[?25h', end='')
        print('\033[2J\033[H', end='')

if __name__ == '__main__':
    # Clear screen
    print('\033[2J\033[H', end='')
    print("flow.py - Press Ctrl+C to exit")
    time.sleep(1)
    run()
