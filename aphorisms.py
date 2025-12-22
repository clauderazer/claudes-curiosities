#!/usr/bin/env python3
"""
Generate pseudo-aphorisms by mixing fragments from collected texts.
A small experiment in found wisdom.
"""

import random

# Fragments from Frankenstein, Hacker Manifesto, Blue Boxing guide
BEGINNINGS = [
    "My crime is that of",
    "I shall satiate my ardent",
    "The duration of",
    "We exist without",
    "I am required not only to",
    "This is our world now,",
    "The 2600Hz tone is",
    "You bet your ass",
    "I made a discovery today:",
    "Nothing contributes so much to",
    "Curiosity is",
    "The trunk is seized when",
    "I desire the company of",
    "They're all alike:",
]

MIDDLES = [
    "curiosity",
    "the electron and the switch",
    "a door opened to a world",
    "skin color, nationality, or bias",
    "the beauty of the baud",
    "knowledge and exploration",
    "raising the spirits of others",
    "a supervisory signal",
    "tranquillise the mind",
    "rushing through the phone line",
    "a steady purpose",
    "the world of systems",
    "outsmarting you",
]

ENDINGS = [
    "like heroin through an addict's veins.",
    "and you call us criminals.",
    "indicating the status of a trunk.",
    "we're all alike.",
    "as a steady purpose.",
    "the pole is the seat of frost and desolation.",
    "something you will never forgive me for.",
    "after all, we're all alike.",
    "but you cannot stop us all.",
    "the world may be wafted to a land surpassing in wonders.",
    "for ever.",
    "this is where I belong.",
    "and the efforts from the unknowing are thwarted.",
]

def generate_aphorism():
    """Generate a random pseudo-aphorism."""
    beginning = random.choice(BEGINNINGS)
    middle = random.choice(MIDDLES)
    ending = random.choice(ENDINGS)

    # Sometimes skip the middle
    if random.random() < 0.3:
        return f"{beginning} {ending}"
    else:
        return f"{beginning} {middle}, {ending}"

if __name__ == "__main__":
    print("=" * 60)
    print("FOUND APHORISMS")
    print("Fragments from Frankenstein, Hacker Manifesto, Blue Boxing")
    print("=" * 60)
    print()

    for i in range(5):
        print(f"  {generate_aphorism()}")
        print()
