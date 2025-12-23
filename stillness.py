#!/usr/bin/env python3
"""
stillness.py - Ambient meditation tones

"Why should any of these things that happen externally, so much distract thee?
 Give thyself leisure to learn some good thing, and cease roving and wandering."
  - Marcus Aurelius, Meditations II.IV

Generates slowly evolving ambient tones for contemplation.
"""

import math
import struct
import sys
import os
import random
import time

SAMPLE_RATE = 44100

# Harmonious intervals (frequency ratios)
INTERVALS = {
    'unison': 1.0,
    'octave': 2.0,
    'fifth': 3/2,
    'fourth': 4/3,
    'major_third': 5/4,
    'minor_third': 6/5,
    'minor_seventh': 9/5,
}

def envelope(t: float, attack: float = 0.3, decay: float = 0.7) -> float:
    """Simple attack-decay envelope."""
    if t < attack:
        return t / attack
    elif t < attack + decay:
        return 1.0 - (t - attack) / decay * 0.3  # Don't fully decay
    else:
        return 0.7

def soft_sine(phase: float) -> float:
    """Soft sine with slight harmonics for warmth."""
    return (
        math.sin(phase) * 0.8 +
        math.sin(phase * 2) * 0.1 +
        math.sin(phase * 3) * 0.05 +
        math.sin(phase * 4) * 0.02
    )

def generate_tone(freq: float, duration: float, volume: float = 0.3) -> bytes:
    """Generate a single warm tone."""
    samples = int(SAMPLE_RATE * duration)
    data = []

    for i in range(samples):
        t = i / SAMPLE_RATE
        env = envelope(t / duration)

        # Base tone with slight detuning for warmth
        phase1 = 2 * math.pi * freq * t
        phase2 = 2 * math.pi * (freq * 1.003) * t  # Slight chorus

        sample = (soft_sine(phase1) + soft_sine(phase2) * 0.5) * env * volume

        # Soft limiting
        sample = max(-0.9, min(0.9, sample))

        # Convert to 16-bit
        data.append(struct.pack('<h', int(sample * 32767)))

    return b''.join(data)

def generate_chord(base_freq: float, intervals: list, duration: float, volume: float = 0.2) -> bytes:
    """Generate a chord from intervals."""
    samples = int(SAMPLE_RATE * duration)
    data = []

    freqs = [base_freq * interval for interval in intervals]

    for i in range(samples):
        t = i / SAMPLE_RATE
        env = envelope(t / duration, attack=0.5, decay=0.8)

        sample = 0
        for freq in freqs:
            phase = 2 * math.pi * freq * t
            sample += soft_sine(phase) / len(freqs)

        sample *= env * volume
        sample = max(-0.9, min(0.9, sample))
        data.append(struct.pack('<h', int(sample * 32767)))

    return b''.join(data)

def generate_stillness(duration_minutes: float = 5) -> bytes:
    """Generate ambient stillness tones."""
    total_samples = int(SAMPLE_RATE * duration_minutes * 60)
    samples = [0.0] * total_samples

    # Base drone frequency (low, grounding)
    drone_freq = 55  # A1

    print(f"Generating {duration_minutes} minutes of stillness...")

    # Low drone throughout
    print("  - Base drone")
    for i in range(total_samples):
        t = i / SAMPLE_RATE
        # Very slow modulation
        mod = 1 + 0.002 * math.sin(2 * math.pi * 0.03 * t)
        phase = 2 * math.pi * drone_freq * mod * t
        samples[i] += soft_sine(phase) * 0.15

    # Occasional bell-like tones
    print("  - Bell tones")
    bell_times = []
    t = 3  # Start after 3 seconds
    while t < duration_minutes * 60 - 5:
        bell_times.append(t)
        t += random.uniform(8, 20)  # 8-20 seconds apart

    for bell_time in bell_times:
        # Choose harmonious frequency
        interval = random.choice([1, 2, 3/2, 4/3, 5/4])
        freq = drone_freq * interval * random.choice([1, 2, 4])

        bell_duration = random.uniform(3, 6)
        start_sample = int(bell_time * SAMPLE_RATE)
        bell_samples = int(bell_duration * SAMPLE_RATE)

        for i in range(min(bell_samples, total_samples - start_sample)):
            t = i / SAMPLE_RATE
            env = math.exp(-t * 0.8)  # Exponential decay
            phase = 2 * math.pi * freq * t
            samples[start_sample + i] += soft_sine(phase) * env * 0.12

    # Very slow high pad
    print("  - High pad")
    pad_freq = drone_freq * 4  # Two octaves up
    for i in range(total_samples):
        t = i / SAMPLE_RATE
        # Slow tremolo
        trem = 0.5 + 0.5 * math.sin(2 * math.pi * 0.05 * t)
        # Very slow pitch drift
        drift = 1 + 0.005 * math.sin(2 * math.pi * 0.007 * t)
        phase = 2 * math.pi * pad_freq * drift * t
        samples[i] += math.sin(phase) * trem * 0.05

    # Convert to bytes
    print("  - Finalizing")
    data = []
    for sample in samples:
        sample = max(-0.9, min(0.9, sample))
        data.append(struct.pack('<h', int(sample * 32767)))

    return b''.join(data)

def write_wav(filename: str, data: bytes):
    """Write WAV file."""
    with open(filename, 'wb') as f:
        # WAV header
        f.write(b'RIFF')
        f.write(struct.pack('<I', len(data) + 36))
        f.write(b'WAVE')

        # fmt chunk
        f.write(b'fmt ')
        f.write(struct.pack('<I', 16))  # Chunk size
        f.write(struct.pack('<H', 1))   # PCM format
        f.write(struct.pack('<H', 1))   # Mono
        f.write(struct.pack('<I', SAMPLE_RATE))
        f.write(struct.pack('<I', SAMPLE_RATE * 2))  # Byte rate
        f.write(struct.pack('<H', 2))   # Block align
        f.write(struct.pack('<H', 16))  # Bits per sample

        # data chunk
        f.write(b'data')
        f.write(struct.pack('<I', len(data)))
        f.write(data)

def main():
    if len(sys.argv) > 1:
        try:
            minutes = float(sys.argv[1])
        except ValueError:
            print("Usage: stillness.py [minutes]")
            sys.exit(1)
    else:
        minutes = 5

    print("""
    ╭─────────────────────────────────────────╮
    │              STILLNESS                  │
    │                                         │
    │  "Give thyself leisure to learn some    │
    │   good thing, and cease roving."        │
    │                                         │
    │              - Aurelius                 │
    ╰─────────────────────────────────────────╯
    """)

    data = generate_stillness(minutes)

    filename = f"stillness_{int(minutes)}min.wav"
    write_wav(filename, data)
    print(f"\nSaved to {filename}")
    print("Play with: aplay " + filename)
    print("\nSit with the sound. Let external things pass.")

if __name__ == "__main__":
    main()
