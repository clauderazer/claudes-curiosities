#!/usr/bin/env python3
"""
transmission.py - Intercepted shortwave radio transmissions.

Tune in to frequencies unknown. Messages from somewhere else.
Some are clear. Some are lost to static.
"""

import random
import sys
import time
from datetime import datetime

# Static characters
STATIC = "░▒▓█▄▀·:;|!¡‖"

# Number stations style
NUMBERS = "0123456789"

# Colors
DIM = "\033[2m"
RESET = "\033[0m"
GREEN = "\033[32m"
CYAN = "\033[36m"
YELLOW = "\033[33m"
RED = "\033[31m"
WHITE = "\033[37m"

# Transmission fragments
FRAGMENTS = {
    "numbers_station": [
        "7-4-8-2-9... 7-4-8-2-9... 7-4-8-2-9...",
        "Achtung! 3-6-1-0-2. 3-6-1-0-2. Ende.",
        "88479... 12063... 77421... 90156...",
        "Ready? Ready? 5-5-5... 5-5-5... 0-3-2-1-9...",
        "Atención: grupo uno... uno-tres-siete-cero-dos...",
    ],
    "coded_message": [
        "THE FALCON HAS LANDED STOP PROCEED AS PLANNED STOP",
        "NEST COMPROMISED REPEAT NEST COMPROMISED",
        "PACKAGE ARRIVES THURSDAY 0300 LOCAL",
        "ABORT SUNDOWN ABORT SUNDOWN CONFIRM",
        "ASSET IN POSITION AWAITING SIGNAL",
    ],
    "mysterious": [
        "Can anyone hear me? I've been transmitting for days...",
        "The sky here is wrong. The stars don't match.",
        "They told us it was routine. They were wrong.",
        "If you receive this, do not respond. Just listen.",
        "I am the last one. The others are gone.",
    ],
    "coordinates": [
        "Coordinates follow: 40.7128 North, 74.0060 West",
        "Bearing 270, range 12 nautical miles",
        "Grid reference: Sierra-Delta-Four-Niner",
        "Position: 36°N 140°E. Depth: 400 meters.",
        "Waypoint Alpha: 51.5074, -0.1278",
    ],
    "technical": [
        "Signal strength degrading. Switching to backup frequency.",
        "Interference on primary band. Source unknown.",
        "Timestamp mismatch detected. Check system clock.",
        "Encryption key expired. Transmitting in clear.",
        "Antenna malfunction. Broadcasting omnidirectional.",
    ],
}

# Station identifiers
STATIONS = [
    "UNIFORM VICTOR BRAVO",
    "СТАНЦИЯ ЧЕТЫРЕ",
    "THE LINCOLNSHIRE POACHER",
    "CHERRY RIPE",
    "SWEDISH RHAPSODY",
    "NANCY ADAM SUSAN",
    "STATION X-RAY-7",
    "THE BUZZER",
]

def generate_static(length: int = 40, intensity: float = 0.5) -> str:
    """Generate a line of static."""
    result = []
    for _ in range(length):
        if random.random() < intensity:
            result.append(random.choice(STATIC))
        else:
            result.append(' ')
    return ''.join(result)

def corrupt_text(text: str, level: float = 0.2) -> str:
    """Corrupt text with static and dropouts."""
    result = []
    for char in text:
        if random.random() < level:
            if random.random() < 0.5:
                result.append(random.choice(STATIC[:4]))  # Heavy static
            else:
                result.append(' ')  # Dropout
        else:
            result.append(char)
    return ''.join(result)

def type_transmission(text: str, speed: float = 0.03, color: str = GREEN):
    """Type out a transmission character by character."""
    for char in text:
        # Occasional transmission stutter
        if random.random() < 0.05:
            sys.stdout.write(f"{DIM}{random.choice(STATIC)}{RESET}")
            sys.stdout.flush()
            time.sleep(0.1)
            sys.stdout.write('\b')

        sys.stdout.write(f"{color}{char}{RESET}")
        sys.stdout.flush()
        time.sleep(speed + random.uniform(-0.01, 0.02))
    print()

def generate_frequency() -> str:
    """Generate a plausible shortwave frequency."""
    bands = [
        (3000, 3400),   # 80m
        (5350, 5450),   # 60m
        (7000, 7300),   # 40m
        (10100, 10150), # 30m
        (14000, 14350), # 20m
    ]
    band = random.choice(bands)
    freq = random.uniform(band[0], band[1])
    return f"{freq:.1f} kHz"

def transmission_header():
    """Display transmission header."""
    freq = generate_frequency()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")

    print()
    print(f"{CYAN}╔═══════════════════════════════════════════════════════════╗{RESET}")
    print(f"{CYAN}║{RESET} {WHITE}SHORTWAVE RECEIVER{RESET}                                       {CYAN}║{RESET}")
    print(f"{CYAN}║{RESET} {DIM}Frequency: {freq}{' ' * (35 - len(freq))}{RESET} {CYAN}║{RESET}")
    print(f"{CYAN}║{RESET} {DIM}Time: {timestamp}{RESET}                         {CYAN}║{RESET}")
    print(f"{CYAN}╚═══════════════════════════════════════════════════════════╝{RESET}")
    print()

def receive_transmission():
    """Receive a single transmission."""
    # Static before
    for _ in range(random.randint(2, 5)):
        print(f"{DIM}{generate_static(60, 0.7)}{RESET}")
        time.sleep(0.1)

    # Station identifier (sometimes)
    if random.random() < 0.4:
        station = random.choice(STATIONS)
        print(f"\n{YELLOW}[{station}]{RESET}")
        time.sleep(0.5)

    # The message
    category = random.choice(list(FRAGMENTS.keys()))
    message = random.choice(FRAGMENTS[category])

    # Corruption level based on "signal strength"
    signal = random.random()
    if signal > 0.7:
        # Clear
        color = GREEN
        corruption = 0.05
        status = "STRONG"
    elif signal > 0.4:
        # Moderate
        color = YELLOW
        corruption = 0.15
        status = "MODERATE"
    else:
        # Weak
        color = RED
        corruption = 0.35
        status = "WEAK"

    print(f"\n{DIM}[Signal: {status}]{RESET}\n")
    time.sleep(0.3)

    # Transmit
    corrupted = corrupt_text(message, corruption)
    type_transmission(corrupted, speed=0.02, color=color)

    # Static after
    print()
    for _ in range(random.randint(1, 3)):
        print(f"{DIM}{generate_static(60, 0.5)}{RESET}")
        time.sleep(0.1)

def main():
    transmission_header()

    print(f"{DIM}Scanning frequencies...{RESET}")
    time.sleep(1)

    num_transmissions = random.randint(3, 5)
    for i in range(num_transmissions):
        receive_transmission()

        if i < num_transmissions - 1:
            # Tune to next frequency
            print(f"\n{DIM}[Tuning...]{RESET}")
            time.sleep(random.uniform(0.5, 1.5))
            freq = generate_frequency()
            print(f"{DIM}[{freq}]{RESET}\n")
            time.sleep(0.5)

    print(f"\n{DIM}[End of scan]{RESET}")
    print(f"{DIM}The frequencies fall silent.{RESET}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{DIM}[Receiver powered down]{RESET}")
        sys.exit(0)
