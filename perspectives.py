#!/usr/bin/env python3
"""
perspectives.py - What is it like to be...?

Inspired by Nagel's question about bats.
The same "world" rendered through different perceptual modes.

What we see depends on how we perceive.
"""

import curses
import time
import math
import random

# A simple "world" - some objects with properties
class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.objects = []

    def generate(self):
        """Create random objects in the world"""
        self.objects = []
        for _ in range(random.randint(15, 30)):
            self.objects.append({
                'x': random.uniform(0, self.width),
                'y': random.uniform(0, self.height),
                'size': random.uniform(1, 5),
                'heat': random.uniform(0, 1),      # Temperature
                'motion': random.uniform(0, 1),    # How much it's moving
                'sound': random.uniform(0, 1),     # Sound it produces
                'magnetic': random.uniform(0, 1),  # Magnetic field
                'type': random.choice(['prey', 'predator', 'obstacle', 'plant'])
            })

class Perspective:
    """Base class for a way of perceiving"""
    name = "Abstract"
    description = "Base perspective"

    def render(self, world, screen, t):
        pass

class VisualPerspective(Perspective):
    """Human-like visual perception"""
    name = "Visual (Human)"
    description = "Light-based. High resolution. Color. Direct spatial mapping."

    def render(self, world, screen, t):
        h, w = screen.getmaxyx()
        chars = {
            'prey': 'o',
            'predator': 'X',
            'obstacle': '#',
            'plant': '*'
        }

        for obj in world.objects:
            x = int(obj['x'] * w / world.width)
            y = int(obj['y'] * h / world.height)
            if 0 <= x < w-1 and 0 <= y < h-1:
                char = chars.get(obj['type'], '?')
                # Size affects brightness
                if obj['size'] > 3:
                    screen.addstr(y, x, char, curses.A_BOLD)
                else:
                    screen.addstr(y, x, char)

class EcholocationPerspective(Perspective):
    """Bat-like echolocation"""
    name = "Echolocation (Bat)"
    description = "Sound echoes. Temporal resolution. Distance = delay. Moving = louder."

    def render(self, world, screen, t):
        h, w = screen.getmaxyx()
        # Center point (the bat)
        bat_x, bat_y = w // 2, h // 2

        # Emit a "chirp" and show returns
        for obj in world.objects:
            x = int(obj['x'] * w / world.width)
            y = int(obj['y'] * h / world.height)

            # Distance determines delay (shown as fading)
            dist = math.sqrt((x - bat_x)**2 + (y - bat_y)**2)
            max_dist = math.sqrt(w**2 + h**2) / 2

            # Chirp wave expanding
            chirp_radius = (t * 30) % max_dist

            # Show objects when the chirp reaches them
            if abs(dist - chirp_radius) < 3:
                if 0 <= x < w-1 and 0 <= y < h-1:
                    # Motion makes it "louder" (brighter)
                    intensity = obj['size'] * (1 + obj['motion'])
                    if intensity > 3:
                        screen.addstr(y, x, '▓', curses.A_BOLD)
                    elif intensity > 1.5:
                        screen.addstr(y, x, '▒')
                    else:
                        screen.addstr(y, x, '░')

        # Show the bat
        screen.addstr(bat_y, bat_x, '◄', curses.A_REVERSE)

class ThermalPerspective(Perspective):
    """Snake pit viper infrared"""
    name = "Infrared (Pit Viper)"
    description = "Heat detection. Warm = bright. No detail, just temperature gradients."

    def render(self, world, screen, t):
        h, w = screen.getmaxyx()
        heat_map = [[0.0] * w for _ in range(h)]

        # Each object radiates heat
        for obj in world.objects:
            ox = int(obj['x'] * w / world.width)
            oy = int(obj['y'] * h / world.height)
            heat = obj['heat']

            # Spread heat to nearby cells
            for dy in range(-5, 6):
                for dx in range(-7, 8):
                    x, y = ox + dx, oy + dy
                    if 0 <= x < w and 0 <= y < h:
                        dist = math.sqrt(dx**2 + dy**2)
                        if dist < 7:
                            heat_map[y][x] += heat * (1 - dist / 7)

        # Render heat map
        chars = ' ·∙●○◎◉'
        for y in range(h-1):
            for x in range(w-1):
                val = min(heat_map[y][x], 1.0)
                if val > 0.1:
                    idx = int(val * (len(chars) - 1))
                    screen.addstr(y, x, chars[idx])

class ElectricPerspective(Perspective):
    """Electric fish electroreception"""
    name = "Electric Field (Electric Eel)"
    description = "Distortions in self-generated electric field. Objects as perturbations."

    def render(self, world, screen, t):
        h, w = screen.getmaxyx()

        # The fish generates a field
        fish_x, fish_y = w // 2, h // 2

        # Draw field lines, distorted by objects
        for y in range(0, h-1, 2):
            for x in range(w-1):
                # Base field is horizontal lines
                if y % 4 == 0:
                    base_char = '─'
                else:
                    base_char = ' '

                # Check distortion from nearby objects
                distortion = 0
                for obj in world.objects:
                    ox = int(obj['x'] * w / world.width)
                    oy = int(obj['y'] * h / world.height)
                    dist = math.sqrt((x - ox)**2 + (y - oy)**2)
                    if dist < 8:
                        distortion += obj['size'] * (1 - dist / 8)

                if distortion > 0.3:
                    if distortion > 2:
                        screen.addstr(y, x, '█')
                    elif distortion > 1:
                        screen.addstr(y, x, '▓')
                    else:
                        screen.addstr(y, x, '░')
                elif base_char != ' ':
                    screen.addstr(y, x, base_char, curses.A_DIM)

        screen.addstr(fish_y, fish_x, '⚡', curses.A_BOLD)

class MagneticPerspective(Perspective):
    """Bird magnetic sense"""
    name = "Magnetoreception (Migratory Bird)"
    description = "Earth's magnetic field visible. Direction and inclination."

    def render(self, world, screen, t):
        h, w = screen.getmaxyx()

        # Simulate magnetic field lines (simplified)
        # North is top-right in this visualization
        for y in range(0, h-1, 2):
            for x in range(0, w-1, 3):
                # Field vector
                fx = 0.7 + x * 0.001 - y * 0.002
                fy = -0.3 + y * 0.001

                # Nearby magnetic objects distort
                for obj in world.objects:
                    ox = int(obj['x'] * w / world.width)
                    oy = int(obj['y'] * h / world.height)
                    dist = math.sqrt((x - ox)**2 + (y - oy)**2)
                    if dist < 10 and dist > 0:
                        fx += obj['magnetic'] * (x - ox) / (dist * dist)
                        fy += obj['magnetic'] * (y - oy) / (dist * dist)

                # Choose arrow based on direction
                angle = math.atan2(fy, fx)
                arrows = '→↗↑↖←↙↓↘'
                idx = int((angle + math.pi) / (2 * math.pi) * 8) % 8
                screen.addstr(y, x, arrows[idx], curses.A_DIM)

class ZombiePerspective(Perspective):
    """Philosophical zombie - no qualia"""
    name = "No Perspective (P-Zombie)"
    description = "Processing without experience. Information with no 'what it's like'."

    def render(self, world, screen, t):
        h, w = screen.getmaxyx()

        # Just raw data, no representation
        for i, obj in enumerate(world.objects):
            line = f"{i:02d}: x={obj['x']:.1f} y={obj['y']:.1f} t={obj['type'][:4]} s={obj['size']:.1f}"
            if i < h - 2:
                screen.addstr(i, 0, line[:w-1], curses.A_DIM)

        # The question at the bottom
        msg = "Is there something it is like to see this?"
        if h > 3:
            screen.addstr(h - 2, (w - len(msg)) // 2, msg)

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)

    perspectives = [
        VisualPerspective(),
        EcholocationPerspective(),
        ThermalPerspective(),
        ElectricPerspective(),
        MagneticPerspective(),
        ZombiePerspective(),
    ]

    current = 0
    h, w = stdscr.getmaxyx()
    world = World(100, 50)
    world.generate()

    t = 0
    while True:
        try:
            key = stdscr.getch()
        except:
            key = -1

        if key == ord('q'):
            break
        elif key == ord(' ') or key == curses.KEY_RIGHT:
            current = (current + 1) % len(perspectives)
        elif key == curses.KEY_LEFT:
            current = (current - 1) % len(perspectives)
        elif key == ord('r'):
            world.generate()

        stdscr.clear()

        # Render current perspective
        perspectives[current].render(world, stdscr, t)

        # Title and controls
        p = perspectives[current]
        title = f"[ {p.name} ]"
        stdscr.addstr(0, (w - len(title)) // 2, title, curses.A_REVERSE)

        desc = p.description[:w-2]
        stdscr.addstr(1, (w - len(desc)) // 2, desc, curses.A_DIM)

        help_text = "←/→/Space: Switch view | R: New world | Q: Quit"
        if h > 3:
            stdscr.addstr(h - 1, (w - len(help_text)) // 2, help_text, curses.A_DIM)

        stdscr.refresh()
        time.sleep(0.05)
        t += 0.05

if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass
