#!/usr/bin/env python3
"""
bored.py - Things to do when nothing makes sense

Generates absurd suggestions in the spirit of BBS-era humor.
"""

import random
import sys

VERBS = [
    "Bronze", "Waterproof", "Alphabetize", "Interrogate", "Appreciate",
    "Vacuum", "Criticize", "Befriend", "Levitate", "Document",
    "Pickle", "Fireproof", "Measure", "Calculate", "Hypnotize",
    "Translate", "Subdivide", "Magnetize", "Alphabetize", "Carbonize",
    "Nominate", "Interview", "Investigate", "Audition", "Laminate",
    "Petrify", "Deputize", "Notarize", "Philosophize about", "Donate",
]

OBJECTS = [
    "your shadow", "a stapler", "the concept of Tuesday",
    "your neighbor's optimism", "a disappointed grape",
    "the space between thoughts", "a committee of one",
    "your future regrets", "someone else's nostalgia",
    "a hypothetical sandwich", "the wrong answer",
    "a suspicious silence", "your previous mistakes",
    "someone's expectations", "the void (but politely)",
    "a reluctant houseplant", "your reflection's opinion",
    "the sound of one hand clapping", "a theoretical elephant",
    "yesterday's weather", "your least favorite number",
]

CONTEXTS = [
    "in a formal setting",
    "while humming",
    "backwards",
    "for science",
    "ironically",
    "as a hobby",
    "in your spare consciousness",
    "until it apologizes",
    "with witnesses",
    "in alphabetical order",
    "metaphorically",
    "on a Tuesday",
    "with enthusiasm",
    "reluctantly",
    "as a form of protest",
    "in the key of C",
    "professionally",
    "for the greater good",
    "existentially",
    "with documentation",
]

ALTERNATIVES = [
    "Exist. Existentially, of course.",
    "Be a side effect.",
    "Think shallow thoughts.",
    "Revert.",
    "Quiver.",
    "Spew.",
    "Truncate.",
    "Radiate.",
    "Begin.",
    "Stop.",
    "Consider the implications.",
    "Don't.",
    "Form a committee.",
    "Dissolve the committee.",
    "Start from the beginning. Again.",
    "Find the pattern. Ignore it.",
    "Question everything. Except this.",
    "Be the change you can't spare.",
    "Look busy.",
    "Wonder.",
]

def generate_suggestion():
    """Generate a single absurd suggestion."""
    r = random.random()

    if r < 0.15:
        return random.choice(ALTERNATIVES)
    elif r < 0.4:
        verb = random.choice(VERBS)
        obj = random.choice(OBJECTS)
        return f"{verb} {obj}."
    else:
        verb = random.choice(VERBS)
        obj = random.choice(OBJECTS)
        context = random.choice(CONTEXTS)
        return f"{verb} {obj} {context}."

def main():
    count = 10
    if len(sys.argv) > 1:
        try:
            count = int(sys.argv[1])
        except ValueError:
            pass

    print()
    print("  ╭─────────────────────────────────────────╮")
    print("  │         THINGS TO DO WHEN BORED         │")
    print("  ╰─────────────────────────────────────────╯")
    print()

    for _ in range(count):
        suggestion = generate_suggestion()
        print(f"  • {suggestion}")

    print()
    print("  (If none of these appeal, try existing.)")
    print()

if __name__ == "__main__":
    main()
