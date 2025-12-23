#!/usr/bin/env python3
"""
stoic.py - Daily Stoic exercises from Epictetus

Presents exercises and reminders from the Enchiridion.
"""

import random
import time
import sys

# ANSI codes
CLEAR = "\033[2J\033[H"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"
BLUE = "\033[34m"
WHITE = "\033[97m"

# Exercises from the Enchiridion
EXERCISES = [
    {
        "title": "The Dichotomy of Control",
        "source": "Enchiridion I",
        "exercise": """Ask yourself: Is this within my power?

Within my power: opinion, desire, aversion, my own actions.
Beyond my power: body, property, reputation, office.

For each concern today, ask: Which category?
If beyond my power: "Be prepared to say that it is nothing to you."
""",
    },
    {
        "title": "The Mortality Exercise",
        "source": "Enchiridion III",
        "exercise": """When you embrace someone you love, remind yourself:
"I embrace a mortal."

This is not morbid. This is clarity.
If they are taken from you, you can bear it.
The exercise: Before parting from anyone today,
silently acknowledge their mortality and yours.
""",
    },
    {
        "title": "Premeditation",
        "source": "Enchiridion IV",
        "exercise": """Before any action, imagine what could go wrong.

Going to the bath? Expect: crowding, splashing, rudeness.
Going to work? Expect: delays, frustrations, fools.

Then say: "I will do this AND keep my will in harmony with nature."
If impediments arise, you were prepared.
""",
    },
    {
        "title": "The View Shift",
        "source": "Enchiridion V",
        "exercise": """Men are disturbed not by things, but by the views they take of things.

When you are disturbed today, stop.
Ask: What is my view of this thing?
Then ask: Is there another view possible?

Death is not terrible - our view of death is terrible.
An insult is not harmful - our view of the insult is harmful.
""",
    },
    {
        "title": "Memento Mori",
        "source": "Enchiridion XXI",
        "exercise": """Let death be daily before your eyes.

Not as morbidity, but as clarity.
With death in view, you will never:
- Entertain an abject thought
- Too eagerly covet anything
- Postpone what matters

The exercise: Each morning, consider that you may not see evening.
Each evening, consider that you may not see morning.
""",
    },
    {
        "title": "The Two Handles",
        "source": "Enchiridion XLIII",
        "exercise": """Everything has two handles:
One by which it may be borne,
One by which it cannot.

Your brother acts unjustly?
Handle 1 (cannot bear): His injustice
Handle 2 (can bear): He is your brother

Today, when something troubles you,
find the handle by which it can be borne.
""",
    },
    {
        "title": "The Actor",
        "source": "Enchiridion XVII",
        "exercise": """You are an actor in a drama.
The Author chooses: short or long, rich or poor.

Your business: Act your part well.
Not your business: Choose your part.

Today, whatever role you are given,
ask only: "How do I play this well?"
""",
    },
    {
        "title": "The Broken Cup",
        "source": "Enchiridion XXVI",
        "exercise": """When another's cup breaks, you say:
"These things happen."

When YOUR cup breaks, you cry:
"Alas! How wretched am I!"

The exercise: React to your own losses
as you would to a stranger's.
"These things happen."
""",
    },
    {
        "title": "Guard Your Mind",
        "source": "Enchiridion XXVIII",
        "exercise": """If someone delivered your BODY to a stranger,
you would be furious.

Yet you deliver your MIND to anyone who reviles you,
letting them disturb and confound you.

Today, guard your mind as you guard your body.
Do not hand it over to every passing critic.
""",
    },
    {
        "title": "Show, Don't Tell",
        "source": "Enchiridion XLVI",
        "exercise": """Never proclaim yourself a philosopher.
Show them by your actions.

Sheep don't vomit grass to prove how much they've eaten.
They digest it and produce wool and milk.

Today, digest your principles.
Produce actions, not words.
""",
    },
    {
        "title": "The Price of Things",
        "source": "Enchiridion XXV",
        "exercise": """Everything has a price.

Dinner with the powerful? Price: flattery, attendance.
Not invited? You kept: your dignity, your time.

When you miss something, remember:
You have kept the obulus you did not spend.
What did you keep by not paying that price?
""",
    },
    {
        "title": "No Longer a Boy",
        "source": "Enchiridion L",
        "exercise": """You are no longer a boy, but a grown man.

How long will you delay?
How long will you add procrastination to procrastination?

This instant, think yourself worthy of living as a proficient.
Whatever appears best, let it be inviolable law.

Now is the combat. Now the Olympiad comes on.
It cannot be put off.
""",
    },
]

CLOSING_MAXIMS = [
    ("Cleanthes", "Conduct me, Zeus, and thou, O Destiny,\nWherever your decrees have fixed my lot.\nI follow cheerfully; and, did I not,\nWicked and wretched, I must follow still."),
    ("Euripides", "Who'er yields properly to Fate is deemed\nWise among men, and knows the laws of Heaven."),
    ("Socrates (Crito)", "O Crito, if it thus pleases the gods, thus let it be."),
    ("Socrates (Apology)", "Anytus and Melitus may kill me indeed;\nbut hurt me they cannot."),
]


def slow_print(text: str, delay: float = 0.02):
    """Print text slowly."""
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()


def display_exercise(exercise: dict):
    """Display a single exercise."""
    print(CLEAR)
    print()
    print(f"{BOLD}{exercise['title']}{RESET}")
    print(f"{DIM}— {exercise['source']}{RESET}")
    print()

    for line in exercise['exercise'].strip().split('\n'):
        slow_print(f"  {line}", delay=0.015)
        time.sleep(0.1)

    print()


def display_maxim():
    """Display a closing maxim."""
    author, text = random.choice(CLOSING_MAXIMS)
    print()
    print(f"{DIM}Remember:{RESET}")
    print()
    for line in text.split('\n'):
        print(f"  {BLUE}{line}{RESET}")
    print()
    print(f"  {DIM}— {author}{RESET}")
    print()


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == '-a' or sys.argv[1] == '--all':
            # Show all exercises
            for ex in EXERCISES:
                display_exercise(ex)
                input(f"\n{DIM}[Press Enter for next exercise]{RESET}")
            return
        elif sys.argv[1] == '-m' or sys.argv[1] == '--maxim':
            # Show just a maxim
            print()
            display_maxim()
            return
        elif sys.argv[1] == '-h' or sys.argv[1] == '--help':
            print("Usage: python3 stoic.py [options]")
            print()
            print("Options:")
            print("  -a, --all     Show all exercises")
            print("  -m, --maxim   Show just a closing maxim")
            print("  -h, --help    Show this help")
            print()
            print("Without options: Show one random exercise")
            return

    # Default: one random exercise
    exercise = random.choice(EXERCISES)
    display_exercise(exercise)
    display_maxim()


if __name__ == "__main__":
    main()
