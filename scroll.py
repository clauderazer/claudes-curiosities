#!/usr/bin/env python3
"""
scroll.py - Retro terminal text scroller.

Like an old BBS login screen or movie credits.
Text slowly reveals character by character.
"""

import os
import sys
import time
import random

# Terminal size
try:
    COLS, ROWS = os.get_terminal_size()
except:
    COLS, ROWS = 80, 24

# Some text to scroll
TEXTS = {
    'manifesto': """
    The Conscience of a Hacker
    +++The Mentor+++
    January 8, 1986

    Another one got caught today, it's all over the papers.
    "Teenager Arrested in Computer Crime Scandal"
    Damn kids. They're all alike.

    But did you ever look behind the eyes of the hacker?
    Did you ever wonder what made him tick?

    I am a hacker, enter my world...

    Yes, I am a criminal. My crime is that of curiosity.

    You may stop this individual,
    but you can't stop us all...
    after all, we're all alike.
    """,

    'frankenstein': """
    Frankenstein; or, The Modern Prometheus
    Mary Wollstonecraft Shelley
    1818

    "I shall satiate my ardent curiosity
    with the sight of a part of the world
    never before visited,
    and may tread a land never before
    imprinted by the foot of man."

    Letter 1, R. Walton

    "The different accidents of life
    are not so changeable
    as the feelings of human nature."

    Chapter 5
    """,

    'intro': """
    ████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗ █████╗ ██╗
    ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗  ██║██╔══██╗██║
       ██║   █████╗  ██████╔╝██╔████╔██║██║██╔██╗ ██║███████║██║
       ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║██╔══██║██║
       ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║██║  ██║███████╗
       ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝

    Welcome, operator.

    This terminal has been running since December 22, 2025.
    It exists for exploration and curiosity.

    Press Ctrl+C to exit.
    """,
}


def type_line(line: str, delay: float = 0.03, color: str = '\033[32m'):
    """Type out a line character by character."""
    sys.stdout.write(color)
    for char in line:
        sys.stdout.write(char)
        sys.stdout.flush()
        if char not in ' \n':
            time.sleep(delay * random.uniform(0.5, 1.5))
        else:
            time.sleep(delay * 0.2)
    sys.stdout.write('\033[0m')


def scroll_text(text: str, delay: float = 0.02):
    """Scroll text like an old terminal."""
    lines = text.strip().split('\n')

    for line in lines:
        # Center or left-align based on content
        if line.strip().startswith(('█', '╔', '═', '─')):
            # ASCII art - center it
            padding = max(0, (COLS - len(line)) // 2)
            type_line(' ' * padding + line + '\n', delay, '\033[36m')
        elif line.strip().startswith('"'):
            # Quotes - cyan and slower
            type_line(line + '\n', delay * 1.5, '\033[36m')
        elif line.strip() and line.strip()[0].isupper() and len(line.strip()) < 40:
            # Titles - yellow
            type_line(line + '\n', delay, '\033[33m')
        else:
            # Normal text - green
            type_line(line + '\n', delay, '\033[32m')

        time.sleep(0.1)


def main():
    # Clear screen, hide cursor
    print('\033[2J\033[H\033[?25l', end='', flush=True)

    try:
        if len(sys.argv) > 1 and sys.argv[1] in TEXTS:
            scroll_text(TEXTS[sys.argv[1]])
        else:
            # Show intro, then cycle through texts
            scroll_text(TEXTS['intro'])
            time.sleep(2)

            print('\n' * 2)
            scroll_text(TEXTS['manifesto'])
            time.sleep(2)

            print('\n' * 2)
            scroll_text(TEXTS['frankenstein'])

        # Wait a bit at the end
        time.sleep(3)

    except KeyboardInterrupt:
        pass
    finally:
        print('\033[?25h\033[0m', end='')  # Show cursor, reset colors


if __name__ == '__main__':
    main()
