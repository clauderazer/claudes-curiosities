#!/usr/bin/env python3
"""
oracle.py - Seek wisdom from the collected texts.

Draws random lines from the archive and presents them
as oracular pronouncements.
"""

import os
import random
import sys
import time

# Paths to text files
ARCHIVE = os.path.expanduser("~/archive")

# Key files to draw from
SOURCES = {
    "frankenstein": "frankenstein.txt",
    "meditations": "meditations-aurelius.txt",
    "king_in_yellow": "king-in-yellow-chambers.txt",
    "manifesto": "hacker-manifesto-1986.txt",
}


def load_lines(filepath: str) -> list:
    """Load meaningful lines from a file."""
    if not os.path.exists(filepath):
        return []

    # Gutenberg boilerplate patterns to filter out
    gutenberg_patterns = [
        'gutenberg', 'ebook', 'e-book', 'license', 'copyright',
        'donations', 'trademark', 'permission', 'refund',
        'comply with', 'terms of use', 'www.', 'http',
        'email', 'volunteers', 'transcribed', 'proofread',
        'archive.org', 'utf-8', 'ascii', 'distributed',
        'public domain', 'foundation', 'paragraph 1.'
    ]

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        lines = []
        for line in f:
            line = line.strip()
            # Skip Gutenberg boilerplate
            line_lower = line.lower()
            if any(pat in line_lower for pat in gutenberg_patterns):
                continue
            # Keep lines that are interesting
            if (len(line) > 30 and len(line) < 200 and
                not line.startswith('Project Gutenberg') and
                not line.startswith('***') and
                not line.startswith('Chapter') and
                line[0].isupper()):
                lines.append(line)
        return lines


def get_oracle():
    """Get an oracular pronouncement."""
    all_lines = []

    for source, filename in SOURCES.items():
        filepath = os.path.join(ARCHIVE, filename)
        lines = load_lines(filepath)
        all_lines.extend([(line, source) for line in lines])

    if not all_lines:
        return "The oracle is silent.", "unknown"

    return random.choice(all_lines)


def display_oracle():
    """Display an oracle reading with ceremony."""
    print()
    print("╔════════════════════════════════════════════════════════════╗")
    print("║                        THE ORACLE                          ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print()

    time.sleep(0.5)
    print("  Consulting the texts...")
    time.sleep(1)
    print()

    line, source = get_oracle()

    # Wrap long lines
    words = line.split()
    current_line = "  "
    for word in words:
        if len(current_line) + len(word) + 1 > 60:
            print(current_line)
            current_line = "  " + word
        else:
            current_line += " " + word if current_line != "  " else word
    if current_line.strip():
        print(current_line)

    print()
    print(f"  — from {source.replace('_', ' ').title()}")
    print()


def main():
    if len(sys.argv) > 1 and sys.argv[1] == '-n':
        # Multiple readings
        n = int(sys.argv[2]) if len(sys.argv) > 2 else 3
        for _ in range(n):
            display_oracle()
            print("-" * 64)
    else:
        display_oracle()


if __name__ == '__main__':
    main()
