#!/usr/bin/env python3
"""
cutup.py - Burroughs-style cut-up text generator.

Inspired by William S. Burroughs and Brion Gysin's cut-up technique:
1. Take sentences from multiple source texts
2. Cut them at random points
3. Recombine the fragments
4. Something unexpected emerges

"When you cut into the present the future leaks out." - WSB
"""

import os
import random
import re
import sys

# Source texts
ARCHIVE = os.path.expanduser("~/archive")
SOURCES = [
    "frankenstein.txt",
    "meditations-aurelius.txt",
    "king-in-yellow-chambers.txt",
    "hacker-manifesto-1986.txt",
]


def load_sentences(filepath: str) -> list:
    """Load sentences from a file."""
    if not os.path.exists(filepath):
        return []

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()

    # Remove Project Gutenberg headers/footers
    if "*** START" in text:
        text = text.split("*** START")[1]
    if "*** END" in text:
        text = text.split("*** END")[0]

    # Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)

    # Filter: keep reasonable length sentences
    good_sentences = []
    for s in sentences:
        s = s.strip()
        s = ' '.join(s.split())  # Normalize whitespace
        if 20 < len(s) < 200 and s[0].isupper():
            good_sentences.append(s)

    return good_sentences


def cut_sentence(sentence: str) -> tuple:
    """Cut a sentence at a random point, return (before, after)."""
    words = sentence.split()
    if len(words) < 4:
        return sentence, ""

    # Cut at a random word boundary (not first or last)
    cut_point = random.randint(2, len(words) - 2)
    before = ' '.join(words[:cut_point])
    after = ' '.join(words[cut_point:])

    return before, after


def generate_cutup(sentences: list, num_cuts: int = 4) -> str:
    """Generate a cut-up poem from source sentences."""
    if len(sentences) < num_cuts:
        return "Not enough source material."

    # Select random sentences
    selected = random.sample(sentences, num_cuts)

    # Cut each one
    fragments = []
    for s in selected:
        before, after = cut_sentence(s)
        fragments.append(before)
        if after:
            fragments.append(after)

    # Shuffle the fragments
    random.shuffle(fragments)

    # Recombine into lines
    lines = []
    current_line = ""

    for frag in fragments:
        if len(current_line) + len(frag) > 70:
            lines.append(current_line.strip())
            current_line = frag
        else:
            current_line += " " + frag

    if current_line.strip():
        lines.append(current_line.strip())

    return '\n'.join(lines)


def main():
    # Load all sentences
    all_sentences = []
    for source in SOURCES:
        filepath = os.path.join(ARCHIVE, source)
        sentences = load_sentences(filepath)
        all_sentences.extend(sentences)

    if not all_sentences:
        print("No source texts found in ~/archive/")
        return

    print(f"Loaded {len(all_sentences)} sentences from {len(SOURCES)} sources")
    print()

    # Number of poems to generate
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 3

    for i in range(n):
        print("═" * 60)
        print(f"  CUT-UP #{i + 1}")
        print("═" * 60)
        print()
        poem = generate_cutup(all_sentences, num_cuts=random.randint(3, 6))
        print(poem)
        print()


if __name__ == '__main__':
    main()
