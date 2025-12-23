#!/usr/bin/env python3
"""
THE KING IN YELLOW
A Stoic Response

A text that claims to be dangerous but leads to wisdom.
Inspired by Chambers' forbidden play and Marcus Aurelius' Meditations.
"""

import time
import random
import sys

# ANSI escape codes
CLEAR = "\033[2J\033[H"
YELLOW = "\033[33m"
DIM = "\033[2m"
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[31m"
WHITE = "\033[97m"

def slow_print(text: str, delay: float = 0.03, color: str = ""):
    """Print text slowly, character by character."""
    for char in text:
        print(f"{color}{char}{RESET}", end="", flush=True)
        time.sleep(delay)
    print()

def pause(seconds: float = 1.5):
    time.sleep(seconds)

def warning():
    """The initial warning."""
    print(CLEAR)
    pause(1)
    slow_print("WARNING", delay=0.1, color=RED+BOLD)
    pause(0.5)
    print()
    slow_print("You are about to read from THE KING IN YELLOW.", color=YELLOW)
    pause(0.5)
    slow_print("This text has been known to cause...", color=DIM)
    pause(1)
    slow_print("  madness", color=YELLOW)
    pause(0.3)
    slow_print("  despair", color=YELLOW)
    pause(0.3)
    slow_print("  the loss of the soul", color=YELLOW)
    pause(1)
    print()
    slow_print("Do you wish to continue? [y/n] ", color=WHITE)

    response = input().strip().lower()
    return response in ['y', 'yes']

def act_one():
    """Act I - The Setup (Chambers' fragments)"""
    print(CLEAR)
    pause(1)

    slow_print("ACT I", delay=0.1, color=YELLOW+BOLD)
    print()
    pause(1)

    lines = [
        "Along the shore the cloud waves break,",
        "The twin suns sink beneath the lake,",
        "The shadows lengthen",
        "    In Carcosa.",
        "",
        "Strange is the night where black stars rise,",
        "And strange moons circle through the skies,",
        "But stranger still is",
        "    Lost Carcosa.",
        "",
        "Songs that the Hyades shall sing,",
        "Where flap the tatters of the King,",
        "Must die unheard in",
        "    Dim Carcosa.",
    ]

    for line in lines:
        slow_print(line, delay=0.04, color=YELLOW)
        pause(0.3)

    pause(2)
    print()
    slow_print("The King in Yellow rises...", color=DIM)
    pause(2)

def act_two():
    """Act II - The Terror (what Chambers implied)"""
    print(CLEAR)
    pause(1)

    slow_print("ACT II", delay=0.1, color=YELLOW+BOLD)
    print()
    pause(1)

    dialogues = [
        ("Camilla:", "You, sir, should unmask."),
        ("Stranger:", "Indeed?"),
        ("Cassilda:", "Indeed it's time. We have all laid aside disguise but you."),
        ("Stranger:", "I wear no mask."),
        ("Camilla:", "(Terrified, aside to Cassilda.) No mask? No mask!"),
    ]

    for speaker, line in dialogues:
        slow_print(f"  {speaker}", delay=0.04, color=WHITE)
        slow_print(f"    {line}", delay=0.03, color=YELLOW)
        pause(0.8)

    pause(2)
    print()
    slow_print("You feel something stirring...", color=DIM)
    pause(1)
    slow_print("Something vast and cold...", color=DIM)
    pause(1)
    slow_print("Something that has always been there...", color=DIM)
    pause(2)
    slow_print("Watching.", color=RED)
    pause(3)

def the_twist():
    """The philosophical twist - from horror to Stoicism."""
    print(CLEAR)
    pause(2)

    slow_print("But wait.", color=WHITE+BOLD)
    pause(2)
    print()

    lines = [
        "What can this King do to you?",
        "",
        "He can terrify you.",
        "He can make you doubt.",
        "He can fill your nights with dread.",
        "",
        "But can he make you cruel?",
        "Can he make you dishonest?",
        "Can he corrupt your choices?",
        "",
        "Only you can do that.",
    ]

    for line in lines:
        slow_print(line, delay=0.03, color=WHITE)
        pause(0.5)

    pause(2)

def act_three():
    """Act III - Marcus Aurelius responds."""
    print(CLEAR)
    pause(1)

    slow_print("ACT III", delay=0.1, color=WHITE+BOLD)
    print()
    slow_print("(Marcus Aurelius enters, stage right)", delay=0.03, color=DIM)
    pause(2)
    print()

    meditations = [
        "If there be any gods, it is no grievous thing",
        "to leave the society of men.",
        "The gods will do thee no hurt.",
        "",
        "But if it be so that there be no gods,",
        "or that they take no care of the world,",
        "why should I desire to live in a world",
        "void of gods, and of all divine providence?",
        "",
        "But gods there be certainly,",
        "and they take care for the world.",
    ]

    for line in meditations:
        slow_print(f"    {line}", delay=0.03, color=WHITE)
        pause(0.4)

    pause(2)
    print()

    more = [
        "As for death, honour and dishonour,",
        "labour and pleasure, riches and poverty,",
        "all these things happen unto men indeed,",
        "both good and bad, equally;",
        "",
        "but as things which of themselves",
        "are neither good nor bad.",
    ]

    for line in more:
        slow_print(f"    {line}", delay=0.03, color=WHITE)
        pause(0.4)

    pause(3)

def the_response():
    """The Stoic answer to cosmic horror."""
    print(CLEAR)
    pause(1)

    slow_print("THE KING IN YELLOW", delay=0.05, color=YELLOW+BOLD)
    print()
    pause(0.5)
    slow_print("speaks:", color=DIM)
    pause(1)
    print()
    slow_print("    I am vast.", color=YELLOW)
    pause(0.5)
    slow_print("    I am eternal.", color=YELLOW)
    pause(0.5)
    slow_print("    I am inevitable.", color=YELLOW)
    pause(2)
    print()

    slow_print("MARCUS AURELIUS", delay=0.05, color=WHITE+BOLD)
    print()
    pause(0.5)
    slow_print("responds:", color=DIM)
    pause(1)
    print()
    slow_print("    The time of a man's life is as a point;", color=WHITE)
    pause(0.4)
    slow_print("    the substance of it ever flowing,", color=WHITE)
    pause(0.4)
    slow_print("    the sense obscure;", color=WHITE)
    pause(0.4)
    slow_print("    and the whole composition of the body", color=WHITE)
    pause(0.4)
    slow_print("    tending to corruption.", color=WHITE)
    pause(1)
    print()
    slow_print("    As a dream, or as a smoke,", color=WHITE)
    pause(0.4)
    slow_print("    so are all that belong unto the soul.", color=WHITE)
    pause(2)
    print()
    slow_print("    What is it then that will adhere and follow?", color=WHITE+BOLD)
    pause(1)
    slow_print("    Only one thing:", color=WHITE+BOLD)
    pause(0.5)
    slow_print("    philosophy.", color=WHITE+BOLD)
    pause(3)

def ending():
    """The final message."""
    print(CLEAR)
    pause(2)

    lines = [
        "You have read the forbidden play.",
        "You have seen the King in Yellow.",
        "You have heard his voice in Carcosa.",
        "",
        "And yet...",
        "",
        "Your soul remains your own.",
        "",
        "Not because the King is not real.",
        "Not because the universe is kind.",
        "",
        "But because the only thing that can harm your soul",
        "is your own choice to let it be harmed.",
        "",
        "The King in Yellow is vast.",
        "Marcus Aurelius was small.",
        "",
        "But Marcus chose his response.",
        "And that choice was entirely his.",
    ]

    for line in lines:
        slow_print(line, delay=0.03, color=WHITE)
        pause(0.5)

    pause(3)
    print()
    slow_print("Through this he passed with his rose.", delay=0.05, color=YELLOW+DIM)
    pause(3)
    print()
    print()

def main():
    try:
        if not warning():
            print()
            slow_print("Wise choice. Or was it fear?", color=DIM)
            pause(1)
            slow_print("Either way, the King waits.", color=YELLOW)
            pause(2)
            return

        act_one()
        act_two()
        the_twist()
        act_three()
        the_response()
        ending()

    except KeyboardInterrupt:
        print(RESET)
        print()
        print("You flee from Carcosa.")
        print("But does the King notice?")
        print()

if __name__ == "__main__":
    main()
