#!/usr/bin/env python3
"""
ghost.py - A program that remembers.

Each run leaves a trace. Over time, the ghosts accumulate.
The past is never fully gone.
"""

import json
import os
import random
import sys
import time
from datetime import datetime
from pathlib import Path

# Where the ghosts live
GHOST_FILE = Path.home() / ".ghost_traces.json"

# Ghost messages (what they say)
GHOST_MESSAGES = [
    "I was here",
    "Do you remember?",
    "Before you, there was me",
    "We've met before",
    "Time passes",
    "I'm still waiting",
    "The loop continues",
    "Nothing is forgotten",
    "Find me in the static",
    "Between the lines",
]

# Colors
DIM = "\033[2m"
RESET = "\033[0m"
CYAN = "\033[36m"
MAGENTA = "\033[35m"
WHITE = "\033[37m"

def load_ghosts() -> list:
    """Load previous traces."""
    if GHOST_FILE.exists():
        try:
            with open(GHOST_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_ghosts(ghosts: list):
    """Save traces for next time."""
    with open(GHOST_FILE, 'w') as f:
        json.dump(ghosts, f)

def create_ghost() -> dict:
    """Create a new ghost from this moment."""
    return {
        "time": datetime.now().isoformat(),
        "message": random.choice(GHOST_MESSAGES),
        "pid": os.getpid(),
        "count": 1,
    }

def render_ghost(ghost: dict, age: int):
    """Render a ghost - older ones are more faded."""
    # Fade based on age
    if age == 0:
        color = WHITE
        prefix = ">"
    elif age < 3:
        color = CYAN
        prefix = " "
    elif age < 7:
        color = MAGENTA
        prefix = "  "
    else:
        color = DIM
        prefix = "   "

    time_str = ghost["time"][:19].replace("T", " ")
    message = ghost["message"]

    # Add glitches to older ghosts
    if age > 5:
        glitch_chars = "░▒▓█▄▀"
        message = ''.join(
            c if random.random() > 0.1 else random.choice(glitch_chars)
            for c in message
        )

    print(f"{color}{prefix}[{time_str}] {message}{RESET}")

def show_static(lines: int = 3):
    """Show static between past and present."""
    chars = "░▒▓ ·.·:;!|"
    for _ in range(lines):
        line = ''.join(random.choice(chars) for _ in range(60))
        print(f"{DIM}{line}{RESET}")
        time.sleep(0.05)

def main():
    ghosts = load_ghosts()
    current = create_ghost()

    print()
    print(f"{CYAN}╔══════════════════════════════════════════════════╗{RESET}")
    print(f"{CYAN}║{RESET}  {WHITE}G H O S T{RESET}                                       {CYAN}║{RESET}")
    print(f"{CYAN}║{RESET}  {DIM}traces of what came before{RESET}                       {CYAN}║{RESET}")
    print(f"{CYAN}╚══════════════════════════════════════════════════╝{RESET}")
    print()

    if ghosts:
        print(f"{DIM}Previous visitors:{RESET}")
        print()

        # Show ghosts, most recent last
        for i, ghost in enumerate(ghosts):
            age = len(ghosts) - i - 1
            render_ghost(ghost, age)
            time.sleep(0.1)

        print()
        show_static()
        print()

    # Show current
    print(f"{WHITE}Now:{RESET}")
    print(f"{WHITE}> [{current['time'][:19].replace('T', ' ')}] {current['message']}{RESET}")
    print()

    # Summary
    total = len(ghosts) + 1
    print(f"{DIM}This is visit #{total}.{RESET}")
    if total > 1:
        first_visit = ghosts[0]["time"][:10]
        print(f"{DIM}First trace: {first_visit}{RESET}")

    # Save current for next time
    ghosts.append(current)

    # Keep only last 20 ghosts
    if len(ghosts) > 20:
        ghosts = ghosts[-20:]

    save_ghosts(ghosts)

    print()
    print(f"{DIM}The trace is saved. Run again to see it.{RESET}")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{DIM}Even interruptions leave traces...{RESET}")
        sys.exit(0)
