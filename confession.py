#!/usr/bin/env python3
"""
confession.py - An unreliable narrator.

The program tells you one story. The timestamps tell another.
Pay attention to both.

Inspired by "The Repairer of Reputations" (Chambers, 1895).
"""

import random
import sys
import time
from datetime import datetime, timedelta

# The confession as the narrator remembers it
CONFESSION = [
    ("I remember the evening clearly.", "8:00 PM"),
    ("The weather was pleasant - spring sunshine through the window.", "8:00 PM"),
    ("I was reading in my study when Louis arrived.", "8:15 PM"),
    ("We spoke about his engagement to Constance.", "8:30 PM"),
    ("I congratulated him warmly.", "8:45 PM"),
    ("He left around nine, and I returned to my book.", "9:00 PM"),
    ("I read until midnight, then retired.", "12:00 AM"),
    ("I slept soundly.", "12:30 AM"),
    ("The next morning I heard the news about Dr. Archer.", "8:00 AM"),
    ("Such a tragedy. I had seen him just last week.", "8:05 AM"),
    ("The police came to ask questions.", "10:00 AM"),
    ("I told them exactly what I've told you.", "10:30 AM"),
    ("I was home all evening. Louis can confirm.", "10:35 AM"),
]

# What the timestamps actually say (in small print)
REALITY = {
    "8:00 PM": "Left home via back entrance",
    "8:15 PM": "Arrived at Dr. Archer's residence",
    "8:30 PM": "Inside the house",
    "8:45 PM": "Cellar",
    "9:00 PM": "Returned home",
    "12:00 AM": "Awake. Pacing.",
    "12:30 AM": "Awake. Writing.",
    "8:00 AM": "Destroyed letter",
    "8:05 AM": "Disposed of knife",
    "10:00 AM": "Rehearsing story",
    "10:30 AM": "First lie to police",
    "10:35 AM": "Louis was not there",
}

# Colors
DIM = "\033[2m"
RESET = "\033[0m"
YELLOW = "\033[33m"
RED = "\033[31m"

def clear_screen():
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()

def type_text(text: str, delay: float = 0.03):
    """Typewriter effect."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def show_timestamp(claimed: str, actual: str, show_reality: bool = False):
    """Show the timestamp - claimed vs actual."""
    if show_reality:
        sys.stdout.write(f"{DIM}[{claimed}]{RESET} ")
        # Small, dim alternate reality
        sys.stdout.write(f"{DIM}({actual}){RESET}\n")
    else:
        sys.stdout.write(f"{DIM}[{claimed}]{RESET}\n")

def main():
    clear_screen()

    print(f"{YELLOW}═══════════════════════════════════════════════════════════════{RESET}")
    print(f"{YELLOW}                        A CONFESSION{RESET}")
    print(f"{YELLOW}═══════════════════════════════════════════════════════════════{RESET}")
    print()
    time.sleep(1)

    # First pass: the narrator's version
    print("From the deposition of H. Castaigne, April 1920:\n")
    time.sleep(0.5)

    for statement, timestamp in CONFESSION:
        show_timestamp(timestamp, REALITY[timestamp], show_reality=False)
        type_text(statement, delay=0.02)
        time.sleep(0.3)

    print()
    print(f"{DIM}[End of deposition]{RESET}")
    print()
    time.sleep(2)

    # The reveal
    print(f"\n{RED}═══════════════════════════════════════════════════════════════{RESET}")
    print(f"{RED}                    EDITOR'S RECONSTRUCTION{RESET}")
    print(f"{RED}═══════════════════════════════════════════════════════════════{RESET}")
    print()
    print(f"{DIM}Based on evidence discovered in the Castaigne apartment,")
    print(f"the actual timeline appears to have been:{RESET}\n")
    time.sleep(1)

    for statement, timestamp in CONFESSION:
        actual = REALITY[timestamp]
        print(f"{DIM}[{timestamp}]{RESET} {RED}{actual}{RESET}")
        time.sleep(0.4)

    print()
    print(f"{DIM}Mr. Castaigne was found deceased in the Asylum for Criminal Insane.{RESET}")
    print()

    # Final ambiguity
    time.sleep(2)
    print(f"\n{YELLOW}═══════════════════════════════════════════════════════════════{RESET}")
    print(f"{DIM}Which version is true?{RESET}")
    print(f"{DIM}The narrator believed his absolutely.{RESET}")
    print(f"{YELLOW}═══════════════════════════════════════════════════════════════{RESET}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{RESET}")
        sys.exit(0)
