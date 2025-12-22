#!/usr/bin/env python3
"""
mandelbrot.py - Generate a Mandelbrot set image.

The infinite complexity at the boundary.
Outputs a PPM file that can be viewed with any image viewer.
"""

import sys
from typing import Tuple

def mandelbrot(c: complex, max_iter: int = 100) -> int:
    """Calculate escape iteration for a point in the complex plane."""
    z = 0
    for n in range(max_iter):
        if abs(z) > 2:
            return n
        z = z * z + c
    return max_iter

def get_color(iterations: int, max_iter: int) -> Tuple[int, int, int]:
    """Convert iteration count to RGB color."""
    if iterations == max_iter:
        return (0, 0, 0)  # Inside the set: black

    # Color gradient based on iteration count
    t = iterations / max_iter

    # Smooth coloring with sinusoidal waves
    r = int(255 * (0.5 + 0.5 * (t * 3.14159 * 2)))
    r = int(9 * (1 - t) * t * t * t * 255)
    g = int(15 * (1 - t) * (1 - t) * t * t * 255)
    b = int(8.5 * (1 - t) * (1 - t) * (1 - t) * t * 255)

    return (min(255, r), min(255, g), min(255, b))

def generate_mandelbrot(width: int = 800, height: int = 600,
                        x_center: float = -0.5, y_center: float = 0.0,
                        zoom: float = 1.0, max_iter: int = 100) -> list:
    """Generate Mandelbrot set pixel data."""
    pixels = []

    # Calculate viewport bounds
    aspect = width / height
    x_range = 3.5 / zoom
    y_range = x_range / aspect

    x_min = x_center - x_range / 2
    x_max = x_center + x_range / 2
    y_min = y_center - y_range / 2
    y_max = y_center + y_range / 2

    print(f"Generating {width}x{height} image...", file=sys.stderr)
    print(f"Region: ({x_min:.6f}, {y_min:.6f}) to ({x_max:.6f}, {y_max:.6f})", file=sys.stderr)

    for y in range(height):
        if y % 100 == 0:
            print(f"  Row {y}/{height}...", file=sys.stderr)
        row = []
        for x in range(width):
            # Map pixel to complex plane
            real = x_min + (x / width) * (x_max - x_min)
            imag = y_min + (y / height) * (y_max - y_min)
            c = complex(real, imag)

            iterations = mandelbrot(c, max_iter)
            color = get_color(iterations, max_iter)
            row.append(color)
        pixels.append(row)

    return pixels

def write_ppm(filename: str, pixels: list):
    """Write pixels to a PPM file."""
    height = len(pixels)
    width = len(pixels[0])

    with open(filename, 'w') as f:
        f.write(f"P3\n")
        f.write(f"{width} {height}\n")
        f.write(f"255\n")

        for row in pixels:
            for r, g, b in row:
                f.write(f"{r} {g} {b}\n")

    print(f"Wrote {filename}", file=sys.stderr)

def main():
    print("=" * 60)
    print("MANDELBROT SET GENERATOR")
    print("The boundary between stability and chaos.")
    print("=" * 60)
    print()

    # Parameters
    width = 640
    height = 480
    max_iter = 100

    # Different interesting regions
    regions = [
        ("mandelbrot_full.ppm", -0.5, 0.0, 1.0, "Full set"),
        ("mandelbrot_seahorse.ppm", -0.745, 0.1, 20.0, "Seahorse Valley"),
        ("mandelbrot_spiral.ppm", -0.7463, 0.1102, 200.0, "Spiral arm"),
    ]

    for filename, x, y, zoom, name in regions:
        print(f"\nGenerating: {name}")
        pixels = generate_mandelbrot(width, height, x, y, zoom, max_iter)
        write_ppm(filename, pixels)

    print("\n" + "=" * 60)
    print("Images saved as PPM files.")
    print("View with: feh mandelbrot_full.ppm")
    print("Or convert: convert mandelbrot_full.ppm mandelbrot_full.png")
    print("=" * 60)

if __name__ == "__main__":
    main()
