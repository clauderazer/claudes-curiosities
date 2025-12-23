#!/usr/bin/env python3
"""
moors.py - The Enchanted Moors

"To come is easy and takes hours; to go is different—and may take centuries."

Walk through the endless moorland. You may find things.
You may find them again. Time works differently here.
"""

import os
import sys
import time
import random
import math
from dataclasses import dataclass
from typing import Optional

# Colors
GREY = "\033[38;5;247m"
GREEN = "\033[38;5;22m"
PURPLE = "\033[38;5;96m"  # Heather
YELLOW = "\033[38;5;228m"  # Gorse
BLUE = "\033[38;5;67m"   # Mist
WHITE = "\033[38;5;255m"
DIM = "\033[2m"
RESET = "\033[0m"

# Terrain elements
HEATHER = f"{PURPLE}~{RESET}"
GORSE = f"{YELLOW}*{RESET}"
GRASS = f"{GREEN}.{RESET}"
ROCK = f"{GREY}#{RESET}"
MIST = f"{BLUE}:{RESET}"
EMPTY = " "

@dataclass
class Position:
    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))

class EnchantedMoors:
    def __init__(self, width: int = 60, height: int = 20):
        self.width = width
        self.height = height
        self.pos = Position(0, 0)
        self.steps_taken = 0
        self.found_ruins = False
        self.found_glove = False
        self.seen_falcon = False

        # Track what we've seen
        self.memories = []

        # The enchantment: certain positions loop
        self.loop_frequency = random.randint(50, 150)

    def terrain_at(self, x: int, y: int) -> str:
        """Generate terrain procedurally based on position."""
        # Use position to seed randomness
        seed = (x * 7919 + y * 104729) % 1000000
        random.seed(seed)

        r = random.random()
        if r < 0.02:
            return ROCK
        elif r < 0.15:
            return GORSE
        elif r < 0.35:
            return HEATHER
        elif r < 0.40:
            return MIST
        elif r < 0.75:
            return GRASS
        else:
            return EMPTY

    def is_special_location(self) -> Optional[str]:
        """Check if current position is special."""
        # The ruins appear at specific interval
        if (self.pos.x + self.pos.y) % self.loop_frequency == 0 and self.steps_taken > 20:
            if not self.found_ruins:
                self.found_ruins = True
                return "ruins"
            elif not self.found_glove:
                self.found_glove = True
                return "glove"
            else:
                return "shrine"

        # Falcon sighting (rare)
        seed = (self.pos.x * 31337 + self.pos.y * 65537) % 1000
        if seed == 777 and not self.seen_falcon:
            self.seen_falcon = True
            return "falcon"

        return None

    def render_view(self) -> list:
        """Render the current view of the moors."""
        view = []
        for dy in range(-self.height//2, self.height//2):
            row = ""
            for dx in range(-self.width//2, self.width//2):
                world_x = self.pos.x + dx
                world_y = self.pos.y + dy

                if dx == 0 and dy == 0:
                    row += f"{WHITE}@{RESET}"
                else:
                    row += self.terrain_at(world_x, world_y)
            view.append(row)
        return view

    def render_special(self, what: str) -> list:
        """Render a special discovery."""
        lines = []
        if what == "ruins":
            lines = [
                "",
                f"  {GREY}Through the mist, you see crumbling stones...{RESET}",
                "",
                f"    {DIM}      ╭─╮{RESET}",
                f"    {DIM}     ╱   ╲{RESET}",
                f"    {DIM}    ╱     ╲{RESET}",
                f"    {GREY}   │░░░░░░░│{RESET}",
                f"    {GREY}   │░░   ░░│{RESET}",
                f"    {GREY}   │░     ░│{RESET}",
                f"    {GREY}  ╱░       ░╲{RESET}",
                "",
                f"  {BLUE}Ivy-covered walls. Great trees push through.{RESET}",
                f"  {BLUE}This was a garden once.{RESET}",
                "",
            ]
            self.memories.append("You found ruins overgrown with centuries.")

        elif what == "glove":
            lines = [
                "",
                f"  {WHITE}On a cold stone slab, something catches your eye...{RESET}",
                "",
                f"    {DIM}╭───────────────╮{RESET}",
                f"    {DIM}│   {YELLOW}~{RESET}{DIM}    {YELLOW}~{RESET}{DIM}     │{RESET}",
                f"    {DIM}│  {YELLOW}/~~\\{RESET}{DIM}  {YELLOW}/~\\{RESET}{DIM}   │{RESET}",
                f"    {DIM}│  {WHITE}\\__/{RESET}{DIM}  {WHITE}\\_{RESET}{DIM}    │{RESET}",
                f"    {DIM}│      \\_{RESET}{DIM}      │{RESET}",
                f"    {DIM}╰───────────────╯{RESET}",
                "",
                f"  {WHITE}A woman's glove.{RESET}",
                f"  {WHITE}Still warm.{RESET}",
                f"  {WHITE}Still fragrant.{RESET}",
                "",
                f"  {DIM}She was just here.{RESET}",
                "",
            ]
            self.memories.append("You found a glove, still warm and fragrant.")

        elif what == "shrine":
            lines = [
                "",
                f"  {GREY}You kneel before a crumbling shrine...{RESET}",
                "",
                f"    {DIM}╭─────────────────────────────╮{RESET}",
                f"    {DIM}│     {WHITE}PRAY FOR THE SOUL OF{RESET}{DIM}     │{RESET}",
                f"    {DIM}│  {WHITE}THE DEMOISELLE JEANNE D'YS{RESET}{DIM}  │{RESET}",
                f"    {DIM}│        {WHITE}WHO DIED{RESET}{DIM}              │{RESET}",
                f"    {DIM}│   {WHITE}IN HER YOUTH FOR LOVE OF{RESET}{DIM}   │{RESET}",
                f"    {DIM}│     {WHITE}PHILIP, A STRANGER{RESET}{DIM}       │{RESET}",
                f"    {DIM}│        {WHITE}A.D. 1573{RESET}{DIM}             │{RESET}",
                f"    {DIM}╰─────────────────────────────╯{RESET}",
                "",
            ]
            self.memories.append("You found a shrine from 1573.")

        elif what == "falcon":
            lines = [
                "",
                f"  {BLUE}A shadow passes overhead...{RESET}",
                "",
                f"    {DIM}         .---.{RESET}",
                f"    {DIM}        /     \\{RESET}",
                f"    {DIM}    ---{WHITE}>{RESET}{DIM}       {WHITE}<{RESET}{DIM}---{RESET}",
                f"    {DIM}        \\     /{RESET}",
                f"    {DIM}          \\-/{RESET}",
                "",
                f"  {BLUE}A falcon soars from the ruins,{RESET}",
                f"  {BLUE}mounting in narrowing circles,{RESET}",
                f"  {BLUE}until it fades and vanishes in the clouds.{RESET}",
                "",
            ]
            self.memories.append("You saw a falcon soaring from ancient ruins.")

        return lines

    def format_status(self) -> str:
        """Format the status line."""
        direction = ""
        if self.pos.y < 0:
            direction += "N"
        elif self.pos.y > 0:
            direction += "S"
        if self.pos.x > 0:
            direction += "E"
        elif self.pos.x < 0:
            direction += "W"
        if not direction:
            direction = "?"

        return (f"{DIM}Steps: {self.steps_taken} | "
                f"Position: {direction} | "
                f"[WASD to move, Q to quit]{RESET}")

    def move(self, direction: str) -> bool:
        """Move in a direction. Returns True if moved."""
        old_pos = Position(self.pos.x, self.pos.y)

        if direction == 'w':
            self.pos.y -= 1
        elif direction == 's':
            self.pos.y += 1
        elif direction == 'a':
            self.pos.x -= 1
        elif direction == 'd':
            self.pos.x += 1
        else:
            return False

        self.steps_taken += 1

        # The enchantment: sometimes you end up somewhere unexpected
        if self.steps_taken > 100 and random.random() < 0.03:
            # Loop back to a previous meaningful position
            self.pos.x = random.randint(-50, 50)
            self.pos.y = random.randint(-50, 50)

        return True

def get_key():
    """Get a single keypress."""
    import termios
    import tty
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def clear_screen():
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()

def main():
    moors = EnchantedMoors()

    # Hide cursor
    sys.stdout.write("\033[?25l")
    clear_screen()

    # Opening
    print()
    print(f"  {BLUE}The moors stretch endlessly in every direction.{RESET}")
    print(f"  {BLUE}There is no path. The gorse and heather are thick.{RESET}")
    print(f"  {DIM}To come is easy. To go... may take centuries.{RESET}")
    print()
    print(f"  {DIM}[Press any key to begin]{RESET}")
    get_key()

    try:
        while True:
            clear_screen()

            # Check for special locations
            special = moors.is_special_location()

            if special:
                for line in moors.render_special(special):
                    print(line)
                print(f"  {DIM}[Press any key to continue]{RESET}")
                get_key()
                clear_screen()

            # Render normal view
            view = moors.render_view()
            print()
            for row in view:
                print(f"  {row}")
            print()
            print(f"  {moors.format_status()}")

            # Get input
            key = get_key().lower()

            if key == 'q':
                break
            elif key in 'wasd':
                moors.move(key)

    except KeyboardInterrupt:
        pass

    finally:
        # Show cursor
        sys.stdout.write("\033[?25h")
        clear_screen()

        # Ending
        print()
        print(f"  {BLUE}You turn back.{RESET}")
        print(f"  {BLUE}The moors close behind you.{RESET}")
        print()

        if moors.memories:
            print(f"  {DIM}What you remember:{RESET}")
            for memory in moors.memories:
                print(f"  {DIM}- {memory}{RESET}")
            print()

        if moors.found_glove:
            print(f"  {WHITE}The glove is in your pocket.{RESET}")
            print(f"  {WHITE}It is still warm.{RESET}")
            print()

if __name__ == "__main__":
    main()
