#!/usr/bin/env python3
"""
automata_music.py - Cellular automata as music.

Uses 1D elementary cellular automata (like Rule 110) to generate
binary patterns, then maps those patterns to musical scales.

Each generation becomes a chord or arpeggio.
Time flows vertically as the CA evolves.
"""

import math
import random
import struct
import sys
import wave

SAMPLE_RATE = 44100


def apply_rule(rule: int, left: int, center: int, right: int) -> int:
    """Apply an elementary CA rule to get the next cell state."""
    # The neighborhood is a 3-bit number
    neighborhood = (left << 2) | (center << 1) | right
    # The rule is an 8-bit number where each bit determines output
    return (rule >> neighborhood) & 1


def generate_ca(width: int, generations: int, rule: int = 110,
                initial: list = None) -> list:
    """Generate a 1D cellular automaton."""
    if initial is None:
        # Start with a single cell in the middle
        state = [0] * width
        state[width // 2] = 1
    else:
        state = initial.copy()

    history = [state.copy()]

    for _ in range(generations - 1):
        new_state = [0] * width
        for i in range(width):
            left = state[(i - 1) % width]
            center = state[i]
            right = state[(i + 1) % width]
            new_state[i] = apply_rule(rule, left, center, right)
        state = new_state
        history.append(state.copy())

    return history


def state_to_frequencies(state: list, base_freq: float = 220.0,
                         scale: str = "pentatonic") -> list:
    """Convert a CA state to a list of frequencies."""
    # Pentatonic scale intervals (semitones from root)
    scales = {
        "pentatonic": [0, 2, 4, 7, 9, 12, 14, 16, 19, 21],
        "minor": [0, 2, 3, 5, 7, 8, 10, 12, 14, 15],
        "major": [0, 2, 4, 5, 7, 9, 11, 12, 14, 16],
    }

    intervals = scales.get(scale, scales["pentatonic"])

    frequencies = []
    for i, cell in enumerate(state):
        if cell == 1:
            # Map position to scale note
            note_idx = i % len(intervals)
            octave = i // len(intervals)
            semitones = intervals[note_idx] + (octave * 12)
            freq = base_freq * (2 ** (semitones / 12.0))
            frequencies.append(freq)

    return frequencies


def generate_chord(frequencies: list, duration: float,
                   attack: float = 0.01, release: float = 0.05) -> bytes:
    """Generate a chord from multiple frequencies."""
    n_samples = int(SAMPLE_RATE * duration)
    samples = []

    for i in range(n_samples):
        t = i / SAMPLE_RATE
        sample = 0.0

        # Amplitude envelope
        if t < attack:
            amp = t / attack
        elif t > duration - release:
            amp = (duration - t) / release
        else:
            amp = 1.0

        # Mix all frequencies
        for freq in frequencies:
            # Add some harmonic richness
            sample += math.sin(2 * math.pi * freq * t)
            sample += 0.3 * math.sin(2 * math.pi * freq * 2 * t)  # 2nd harmonic

        # Normalize by number of frequencies
        if frequencies:
            sample = sample / (len(frequencies) * 1.3)

        sample = sample * amp * 0.5
        samples.append(int(max(-32767, min(32767, sample * 32767))))

    return struct.pack(f'{len(samples)}h', *samples)


def generate_arpeggio(frequencies: list, duration: float) -> bytes:
    """Generate an arpeggio (notes played sequentially)."""
    if not frequencies:
        return generate_silence(duration)

    note_duration = duration / len(frequencies)
    audio = b''

    for freq in frequencies:
        audio += generate_chord([freq], note_duration, attack=0.005, release=0.02)

    return audio


def generate_silence(duration: float) -> bytes:
    """Generate silence."""
    n_samples = int(SAMPLE_RATE * duration)
    return struct.pack(f'{n_samples}h', *([0] * n_samples))


def ca_to_music(ca_history: list, note_duration: float = 0.3,
                mode: str = "chord", scale: str = "pentatonic") -> bytes:
    """Convert CA history to audio."""
    audio = b''

    for gen_idx, state in enumerate(ca_history):
        frequencies = state_to_frequencies(state, base_freq=220.0, scale=scale)

        # Limit to avoid cacophony
        frequencies = frequencies[:8]

        if not frequencies:
            audio += generate_silence(note_duration)
        elif mode == "chord":
            audio += generate_chord(frequencies, note_duration)
        else:  # arpeggio
            audio += generate_arpeggio(frequencies, note_duration)

    return audio


def save_wav(filename: str, audio: bytes):
    """Save audio to a WAV file."""
    with wave.open(filename, 'wb') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(SAMPLE_RATE)
        f.writeframes(audio)


def visualize_ca(history: list):
    """Print CA as ASCII art."""
    for state in history:
        line = ''.join('█' if c else ' ' for c in state)
        print(line)


def main():
    # Parse arguments
    rule = int(sys.argv[1]) if len(sys.argv) > 1 else 110
    generations = int(sys.argv[2]) if len(sys.argv) > 2 else 16
    width = int(sys.argv[3]) if len(sys.argv) > 3 else 10

    print(f"Rule {rule}, {generations} generations, width {width}")
    print()

    # Generate CA
    ca = generate_ca(width, generations, rule)

    # Visualize
    print("Cellular Automaton Pattern:")
    visualize_ca(ca)
    print()

    # Generate music
    print("Generating music...")
    audio = ca_to_music(ca, note_duration=0.25, mode="chord", scale="pentatonic")

    # Save
    filename = f"/tmp/rule_{rule}.wav"
    save_wav(filename, audio)
    print(f"Saved to {filename}")

    # Try to play
    import subprocess
    try:
        subprocess.run(['aplay', filename], check=True, capture_output=True)
        print("Playing...")
    except:
        print("Use: aplay " + filename)


if __name__ == '__main__':
    main()
