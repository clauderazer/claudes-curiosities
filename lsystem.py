#!/usr/bin/env python3
"""
L-System generator - simple string rewriting that creates complex structures.

Aristid Lindenmayer invented these to model plant growth.
A few rules, applied repeatedly, create branching forms.

December 22, 2025
"""

import math
import sys

# Some classic L-systems
PRESETS = {
    'tree': {
        'axiom': 'X',
        'rules': {'X': 'F+[[X]-X]-F[-FX]+X', 'F': 'FF'},
        'angle': 25,
        'iterations': 5
    },
    'sierpinski': {
        'axiom': 'F-G-G',
        'rules': {'F': 'F-G+F+G-F', 'G': 'GG'},
        'angle': 120,
        'iterations': 5
    },
    'dragon': {
        'axiom': 'FX',
        'rules': {'X': 'X+YF+', 'Y': '-FX-Y'},
        'angle': 90,
        'iterations': 10
    },
    'plant': {
        'axiom': 'X',
        'rules': {'X': 'F-[[X]+X]+F[+FX]-X', 'F': 'FF'},
        'angle': 22.5,
        'iterations': 5
    },
    'koch': {
        'axiom': 'F',
        'rules': {'F': 'F+F-F-F+F'},
        'angle': 90,
        'iterations': 4
    }
}

def apply_rules(string, rules):
    """Apply L-system rules once."""
    result = []
    for char in string:
        result.append(rules.get(char, char))
    return ''.join(result)

def generate(axiom, rules, iterations):
    """Generate the L-system string."""
    current = axiom
    for _ in range(iterations):
        current = apply_rules(current, rules)
    return current

def turtle_to_points(lstring, angle_deg):
    """Convert L-system string to points using turtle graphics."""
    x, y = 0, 0
    direction = 90  # Start pointing up
    angle = angle_deg
    stack = []
    points = [(x, y)]

    for char in lstring:
        if char in 'FG':  # Move forward
            rad = math.radians(direction)
            x += math.cos(rad)
            y += math.sin(rad)
            points.append((x, y))
        elif char == '+':  # Turn left
            direction += angle
        elif char == '-':  # Turn right
            direction -= angle
        elif char == '[':  # Save state
            stack.append((x, y, direction))
        elif char == ']':  # Restore state
            if stack:
                x, y, direction = stack.pop()
                points.append(None)  # Break in line
                points.append((x, y))

    return points

def render_to_terminal(points, width=80, height=40):
    """Render points to terminal characters."""
    if not points:
        return

    # Filter out None values for bounds calculation
    valid_points = [p for p in points if p is not None]
    if not valid_points:
        return

    # Find bounds
    xs = [p[0] for p in valid_points]
    ys = [p[1] for p in valid_points]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    # Handle degenerate cases
    if max_x == min_x:
        max_x = min_x + 1
    if max_y == min_y:
        max_y = min_y + 1

    # Create grid
    grid = [[' ' for _ in range(width)] for _ in range(height)]

    # Scale and plot points
    for p in valid_points:
        px = int((p[0] - min_x) / (max_x - min_x) * (width - 1))
        py = int((p[1] - min_y) / (max_y - min_y) * (height - 1))
        py = height - 1 - py  # Flip y
        if 0 <= px < width and 0 <= py < height:
            grid[py][px] = '█'

    # Print
    for row in grid:
        print(''.join(row))

def main():
    print("L-System Generator")
    print("=" * 40)
    print()
    print("Available presets:", ', '.join(PRESETS.keys()))
    print()

    # Get preset
    name = sys.argv[1] if len(sys.argv) > 1 else 'plant'
    if name not in PRESETS:
        print(f"Unknown preset: {name}")
        print(f"Available: {', '.join(PRESETS.keys())}")
        sys.exit(1)

    preset = PRESETS[name]
    iterations = int(sys.argv[2]) if len(sys.argv) > 2 else preset['iterations']

    print(f"Generating '{name}' with {iterations} iterations...")
    print(f"Axiom: {preset['axiom']}")
    print(f"Angle: {preset['angle']}°")
    print()

    # Generate
    lstring = generate(preset['axiom'], preset['rules'], iterations)
    print(f"String length: {len(lstring)}")
    print()

    # Render
    points = turtle_to_points(lstring, preset['angle'])
    render_to_terminal(points)
    print()
    print(f"'{name}' - {iterations} iterations")

if __name__ == "__main__":
    main()
