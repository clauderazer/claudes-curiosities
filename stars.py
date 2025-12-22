#!/usr/bin/env python3
"""
stars.py - A 3D starfield flying through space.

Classic demoscene effect: stars streaming past as if you're
traveling through the cosmos.
"""

import os
import sys
import time
import random
from dataclasses import dataclass
from typing import List

# Terminal size
try:
    COLS, ROWS = os.get_terminal_size()
except:
    COLS, ROWS = 80, 24

ROWS -= 1
CENTER_X = COLS // 2
CENTER_Y = ROWS // 2

# Star characters by distance (far to near)
STAR_CHARS = '.·+*#@'

@dataclass
class Star:
    x: float  # -1 to 1
    y: float  # -1 to 1
    z: float  # 0 to 1 (0 = far, 1 = near)

def spawn_star() -> Star:
    """Create a new star at a random position far away."""
    return Star(
        x=random.uniform(-1, 1),
        y=random.uniform(-1, 1),
        z=random.uniform(0.001, 0.1)  # Start far away
    )

def project(star: Star) -> tuple:
    """
    Project a 3D star position to 2D screen coordinates.
    Returns (screen_x, screen_y, brightness) or None if off-screen.
    """
    if star.z <= 0:
        return None

    # Perspective projection
    factor = 1 / star.z

    # Screen coordinates (centered)
    sx = int(CENTER_X + star.x * factor * 2)  # Wider aspect
    sy = int(CENTER_Y + star.y * factor)

    # Check bounds
    if not (0 <= sx < COLS and 0 <= sy < ROWS):
        return None

    # Brightness based on z (closer = brighter)
    brightness = min(1.0, star.z * 3)

    return (sx, sy, brightness)

def run(speed: float = 0.02):
    """Main loop."""
    # Hide cursor
    print('\033[?25l\033[2J', end='', flush=True)

    stars: List[Star] = [spawn_star() for _ in range(200)]
    dt = 0.05

    try:
        while True:
            start = time.time()

            # Create empty screen buffer
            screen = [[' '] * COLS for _ in range(ROWS)]

            # Update and draw stars
            new_stars = []
            for star in stars:
                # Move star closer (increase z)
                star.z += speed

                # Project to screen
                proj = project(star)

                if proj is None:
                    # Star went off screen or behind camera
                    new_stars.append(spawn_star())
                else:
                    sx, sy, brightness = proj
                    # Choose character based on brightness
                    char_idx = int(brightness * (len(STAR_CHARS) - 1))
                    char_idx = max(0, min(len(STAR_CHARS) - 1, char_idx))
                    screen[sy][sx] = STAR_CHARS[char_idx]
                    new_stars.append(star)

            stars = new_stars

            # Render
            frame = '\033[H'
            for row in screen:
                frame += ''.join(row) + '\n'

            sys.stdout.write(frame)
            sys.stdout.flush()

            # Timing
            elapsed = time.time() - start
            if elapsed < dt:
                time.sleep(dt - elapsed)

    except KeyboardInterrupt:
        pass
    finally:
        print('\033[?25h\033[2J\033[H', end='')

if __name__ == '__main__':
    print("stars.py - Flying through space")
    print("Press Ctrl+C to exit")
    time.sleep(1)
    run()
