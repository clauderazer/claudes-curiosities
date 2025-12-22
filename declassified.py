#!/usr/bin/env python3
"""
declassified.py - Generate fake declassified documents.

Creates procedurally generated "official" documents with redactions,
classification stamps, and bureaucratic language.

The truth is in the gaps.
"""

import random
import sys
import time
from datetime import datetime, timedelta

# Document types
DOC_TYPES = [
    "MEMORANDUM",
    "FIELD REPORT",
    "INTELLIGENCE ASSESSMENT",
    "INCIDENT LOG",
    "INTERVIEW TRANSCRIPT",
    "SURVEILLANCE SUMMARY",
    "ASSET EVALUATION",
]

# Classification levels
CLASSIFICATIONS = [
    "CONFIDENTIAL",
    "SECRET",
    "TOP SECRET",
    "TOP SECRET//SCI",
    "TOP SECRET//NOFORN",
]

# Redaction styles
REDACTION = "█"

# Project code names
CODE_NAMES = [
    "LOOKING GLASS", "NORTHERN LIGHTS", "PAPER CLIP", "ARTICHOKE",
    "MIDNIGHT CLIMAX", "CHAOS", "GARDEN PLOT", "CABLE SPLICER",
    "YELLOW KING", "NIGHT CRAWLER", "PALE HORSE", "WINTER FROST",
    "DEEP STATE", "BLUE BOOK", "MONARCH", "STARGATE",
]

# Locations
LOCATIONS = [
    "Site [REDACTED]", "Facility 12", "the Nevada installation",
    "Building 4, [LOCATION REDACTED]", "offshore platform",
    "the mountain complex", "Sublevel 3", "the northern site",
]

# Subjects
SUBJECTS = [
    "Subject", "the asset", "the individual", "the contact",
    "the witness", "the target", "Source DELTA", "Source OMEGA",
]

# Verbs for events
VERBS = [
    "exhibited", "demonstrated", "displayed", "manifested",
    "reported", "claimed", "experienced", "underwent",
]

# Phenomena
PHENOMENA = [
    "unusual cognitive abilities",
    "temporal displacement symptoms",
    "precognitive episodes",
    "anomalous electromagnetic readings",
    "unexplained materialization events",
    "coherent signal reception without equipment",
    "documented remote viewing accuracy",
    "spontaneous [REDACTED] generation",
]

# Recommendations
RECOMMENDATIONS = [
    "continued observation",
    "immediate termination of project",
    "expansion of program scope",
    "transfer to [FACILITY REDACTED]",
    "indefinite containment",
    "release with monitoring",
    "integration into Phase II",
    "classification upgrade",
]

# Colors
DIM = "\033[2m"
BOLD = "\033[1m"
RESET = "\033[0m"
RED = "\033[31m"
YELLOW = "\033[33m"

def redact(text: str, probability: float = 0.3) -> str:
    """Randomly redact portions of text."""
    words = text.split()
    result = []
    for word in words:
        if random.random() < probability:
            result.append(REDACTION * len(word))
        else:
            result.append(word)
    return ' '.join(result)

def partial_redact(text: str) -> str:
    """Partially redact a word, leaving hints."""
    if len(text) < 4:
        return REDACTION * len(text)
    visible = random.randint(1, max(1, len(text) // 3))
    return text[:visible] + REDACTION * (len(text) - visible)

def generate_date() -> str:
    """Generate a plausible past date."""
    year = random.randint(1952, 1995)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return f"{year}-{month:02d}-{day:02d}"

def generate_reference() -> str:
    """Generate a document reference number."""
    prefix = random.choice(["DOC", "REF", "FILE", "MEMO", "CASE"])
    numbers = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    suffix = random.choice(["A", "B", "C", "X", "Z", "-1", "-7"])
    return f"{prefix}-{numbers}{suffix}"

def generate_paragraph() -> str:
    """Generate a paragraph of official-sounding text with redactions."""
    templates = [
        f"On {redact(generate_date())}, {random.choice(SUBJECTS)} {random.choice(VERBS)} {redact(random.choice(PHENOMENA))} at {random.choice(LOCATIONS)}.",
        f"Per directive {generate_reference()}, all personnel assigned to {redact(random.choice(CODE_NAMES))} are hereby {redact('instructed to maintain complete operational security')}.",
        f"The incident on {redact(generate_date())} resulted in {redact('three casualties')} and {redact('significant structural damage')} to {random.choice(LOCATIONS)}.",
        f"Analysis of recovered materials indicates {redact(random.choice(PHENOMENA))}. Further testing is {redact('not recommended')} at this time.",
        f"{random.choice(SUBJECTS)} was {redact('terminated')} on {redact(generate_date())} following {redact('breach of containment protocols')}.",
        f"Budget allocation for {redact(random.choice(CODE_NAMES))} increased by {redact('340%')} in fiscal year {redact(str(random.randint(1960, 1989)))}.",
        f"Note: {random.choice(SUBJECTS)} expressed {redact('extreme distress')} during {redact('enhanced interrogation')}. Recommend {redact(random.choice(RECOMMENDATIONS))}.",
        f"Contact with {redact('external entities')} was established on {redact(generate_date())}. Communication was {redact('brief')} and {redact('disturbing')}.",
    ]
    return random.choice(templates)

def generate_document():
    """Generate a complete fake declassified document."""
    doc_type = random.choice(DOC_TYPES)
    classification = random.choice(CLASSIFICATIONS)
    code_name = random.choice(CODE_NAMES)
    date = generate_date()
    ref = generate_reference()

    # Header
    print(f"\n{BOLD}{'=' * 70}{RESET}")
    print(f"{RED}{classification}{RESET}")
    print(f"{BOLD}{'=' * 70}{RESET}\n")

    print(f"{BOLD}{doc_type}{RESET}")
    print(f"Date: {date}")
    print(f"Reference: {ref}")
    print(f"Project: {redact(code_name)}")
    print(f"Prepared by: {REDACTION * 15}")
    print()

    # Body
    print(f"{DIM}SUBJECT: Operations Summary - {partial_redact(code_name)}{RESET}")
    print()

    num_paragraphs = random.randint(3, 6)
    for _ in range(num_paragraphs):
        print(generate_paragraph())
        print()

    # Conclusion/Recommendation
    print(f"{BOLD}RECOMMENDATION:{RESET}")
    print(f"Based on the above findings, this office recommends {redact(random.choice(RECOMMENDATIONS))}.")
    print()

    # Classification footer
    print(f"{DIM}This document has been partially declassified pursuant to")
    print(f"Executive Order {random.randint(10000, 13999)}.")
    print(f"Portions remain classified {classification}.{RESET}")
    print()

    print(f"{BOLD}{'=' * 70}{RESET}")
    print(f"{RED}{classification}{RESET}")
    print(f"{BOLD}{'=' * 70}{RESET}\n")

    # Handwritten note (sometimes)
    if random.random() < 0.4:
        notes = [
            "They know. -J",
            "Destroy after reading",
            "See also: file 77-B",
            "This isn't over",
            "Who authorized this?",
            "The dates don't match",
            "Check the basement",
        ]
        print(f"{DIM}[Handwritten note in margin: \"{random.choice(notes)}\"]{RESET}\n")

def main():
    print(f"\n{YELLOW}DECLASSIFIED DOCUMENT GENERATOR{RESET}")
    print(f"{DIM}The truth is in the gaps.{RESET}\n")

    num_docs = 3
    for i in range(num_docs):
        generate_document()
        if i < num_docs - 1:
            print(f"\n{DIM}--- Next document ---{RESET}\n")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{RESET}[DOCUMENT RETRIEVAL CANCELLED]")
        sys.exit(0)
