#!/usr/bin/env python3
"""
rain.py - Rain falling in the terminal.

Simple, meditative. Drops fall, splash at the bottom, repeat.
"""

import os
import random
import sys
import time

# Rain characters with varying intensity
DROPS = ['|', '│', '┃', '╎', '╏', '┆', '┇', '┊', '┋']
SPLASH = ['·', '∙', '•', '○', '◦', '°']

# Colors: grays and blues
COLORS = [
    "\033[38;5;240m",  # Dark gray
    "\033[38;5;244m",  # Gray
    "\033[38;5;248m",  # Light gray
    "\033[38;5;67m",   # Muted blue
    "\033[38;5;68m",   # Blue
    "\033[38;5;110m",  # Light blue
]

RESET = "\033[0m"


def get_terminal_size():
    try:
        size = os.get_terminal_size()
        return size.columns, size.lines - 1
    except OSError:
        return 80, 24


class Drop:
    def __init__(self, x: int, height: int):
        self.x = x
        self.y = 0
        self.height = height
        self.speed = random.uniform(0.5, 2.0)
        self.char = random.choice(DROPS)
        self.color = random.choice(COLORS)
        self.length = random.randint(1, 3)

    def update(self) -> bool:
        """Update position. Returns False if drop is done."""
        self.y += self.speed
        return self.y < self.height + self.length

    def render(self, screen: list):
        """Render drop onto screen buffer."""
        for i in range(self.length):
            y = int(self.y) - i
            if 0 <= y < len(screen):
                if 0 <= self.x < len(screen[y]):
                    # Fade effect for trail
                    if i == 0:
                        screen[y][self.x] = f"{self.color}{self.char}{RESET}"
                    else:
                        fade = COLORS[max(0, COLORS.index(self.color) - i)]
                        screen[y][self.x] = f"{fade}{random.choice(DROPS[:3])}{RESET}"


class Splash:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.life = 3
        self.char = random.choice(SPLASH)

    def update(self) -> bool:
        self.life -= 1
        return self.life > 0

    def render(self, screen: list):
        if 0 <= self.y < len(screen) and 0 <= self.x < len(screen[self.y]):
            color = COLORS[min(self.life, len(COLORS) - 1)]
            screen[self.y][self.x] = f"{color}{self.char}{RESET}"


def main():
    width, height = get_terminal_size()

    drops = []
    splashes = []

    # Hide cursor, clear screen
    sys.stdout.write("\033[?25l")
    sys.stdout.write("\033[2J")

    # Rain density
    drop_chance = 0.3

    try:
        while True:
            # Create screen buffer
            screen = [[' '] * width for _ in range(height)]

            # Maybe add new drops
            for x in range(width):
                if random.random() < drop_chance / width:
                    drops.append(Drop(x, height))

            # Update and render drops
            new_drops = []
            for drop in drops:
                if drop.update():
                    drop.render(screen)
                    new_drops.append(drop)
                else:
                    # Create splash
                    splashes.append(Splash(drop.x, height - 1))
            drops = new_drops

            # Update and render splashes
            new_splashes = []
            for splash in splashes:
                if splash.update():
                    splash.render(screen)
                    new_splashes.append(splash)
            splashes = new_splashes

            # Draw screen
            sys.stdout.write("\033[H")
            for row in screen:
                sys.stdout.write(''.join(row) + '\n')
            sys.stdout.flush()

            time.sleep(0.05)

    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write("\033[?25h")
        sys.stdout.write(RESET)
        sys.stdout.write("\033[2J\033[H")
        print("Rain stopped.")


if __name__ == "__main__":
    main()
