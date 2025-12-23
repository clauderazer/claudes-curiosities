#!/usr/bin/env python3
"""
breathe.py - A breathing meditation.

Inhale... hold... exhale... hold...
Watch the circle expand and contract.
"""

import math
import os
import sys
import time

# Breathing pattern (seconds)
INHALE = 4
HOLD_IN = 4
EXHALE = 4
HOLD_OUT = 4

# Colors
COLORS = [
    "\033[38;5;23m",   # Deep teal
    "\033[38;5;29m",   # Teal
    "\033[38;5;36m",   # Cyan-ish
    "\033[38;5;43m",   # Light cyan
    "\033[38;5;50m",   # Pale cyan
    "\033[38;5;51m",   # Bright cyan
]

RESET = "\033[0m"
DIM = "\033[2m"

def get_terminal_size():
    try:
        size = os.get_terminal_size()
        return size.columns, size.lines
    except:
        return 80, 24

def draw_circle(cx: int, cy: int, radius: float, width: int, height: int) -> list:
    """Draw a circle with the given radius."""
    screen = [[' ' for _ in range(width)] for _ in range(height)]

    # Character aspect ratio compensation
    aspect = 2.0

    for angle in range(360):
        rad = math.radians(angle)
        x = int(cx + radius * math.cos(rad) * aspect)
        y = int(cy + radius * math.sin(rad))

        if 0 <= x < width and 0 <= y < height:
            # Color based on radius
            color_idx = min(int(radius / 2), len(COLORS) - 1)
            screen[y][x] = f"{COLORS[color_idx]}●{RESET}"

    return screen

def render_screen(screen: list):
    """Render the screen buffer."""
    sys.stdout.write("\033[H")
    for row in screen:
        sys.stdout.write(''.join(row) + '\n')
    sys.stdout.flush()

def show_instruction(text: str, width: int, y: int):
    """Show centered instruction."""
    x = (width - len(text)) // 2
    sys.stdout.write(f"\033[{y};{x}H{DIM}{text}{RESET}")
    sys.stdout.flush()

def breathe_cycle(width: int, height: int, cx: int, cy: int):
    """One complete breath cycle."""
    max_radius = min(width // 4, height // 2) - 2
    min_radius = 2

    fps = 30

    # Inhale - expand
    show_instruction("Breathe in...", width, 2)
    frames = INHALE * fps
    for i in range(frames):
        t = i / frames
        radius = min_radius + (max_radius - min_radius) * t
        screen = draw_circle(cx, cy, radius, width, height)
        render_screen(screen)
        time.sleep(1 / fps)

    # Hold in
    show_instruction("Hold...", width, 2)
    time.sleep(HOLD_IN)

    # Exhale - contract
    show_instruction("Breathe out...", width, 2)
    frames = EXHALE * fps
    for i in range(frames):
        t = i / frames
        radius = max_radius - (max_radius - min_radius) * t
        screen = draw_circle(cx, cy, radius, width, height)
        render_screen(screen)
        time.sleep(1 / fps)

    # Hold out
    show_instruction("Hold...", width, 2)
    time.sleep(HOLD_OUT)

def main():
    width, height = get_terminal_size()
    cx = width // 2
    cy = height // 2

    # Setup
    sys.stdout.write("\033[2J")  # Clear
    sys.stdout.write("\033[?25l")  # Hide cursor

    try:
        while True:
            breathe_cycle(width, height, cx, cy)
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write("\033[?25h")  # Show cursor
        sys.stdout.write("\033[2J\033[H")
        print(f"{DIM}Breathe easy.{RESET}")

if __name__ == "__main__":
    main()
