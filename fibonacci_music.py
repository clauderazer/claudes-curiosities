#!/usr/bin/env python3
"""
Music from mathematics - the Fibonacci sequence as melody.

Each number maps to a note. 1 2 3 5 8 13 21 34...
Patterns emerge from pure arithmetic.

December 22, 2025
"""

import wave
import struct
import math

def generate_tone(frequency, duration, sample_rate=44100, amplitude=0.3):
    """Generate samples for a sine wave with harmonics."""
    samples = []
    num_samples = int(duration * sample_rate)

    for i in range(num_samples):
        t = i / sample_rate
        # Fundamental + harmonics for richer tone
        value = amplitude * (
            0.6 * math.sin(2 * math.pi * frequency * t) +
            0.3 * math.sin(4 * math.pi * frequency * t) +  # octave
            0.1 * math.sin(6 * math.pi * frequency * t)    # fifth above octave
        )
        # Envelope
        attack = min(1.0, i / (0.05 * sample_rate))
        decay = min(1.0, (num_samples - i) / (0.1 * sample_rate))
        value *= attack * decay
        samples.append(value)

    return samples

def fibonacci(n):
    """Generate first n Fibonacci numbers."""
    fibs = [1, 1]
    while len(fibs) < n:
        fibs.append(fibs[-1] + fibs[-2])
    return fibs

def number_to_note(num, base_freq=220):
    """Map a number to a frequency using modular arithmetic."""
    # Use mod 12 to stay within an octave, then map to chromatic scale
    semitones = num % 12
    # 2^(n/12) gives the frequency ratio
    return base_freq * (2 ** (semitones / 12))

def samples_to_wav(samples, filename, sample_rate=44100):
    """Write samples to a WAV file."""
    with wave.open(filename, 'w') as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)

        for sample in samples:
            packed = struct.pack('<h', int(max(-1, min(1, sample)) * 32767))
            wav.writeframes(packed)

def main():
    sample_rate = 44100
    fibs = fibonacci(30)

    print("Fibonacci sequence:", fibs[:15], "...")
    print("Mapping to notes...")

    all_samples = []
    duration = 0.3  # seconds per note

    for i, num in enumerate(fibs):
        freq = number_to_note(num)
        # Vary duration slightly based on position
        dur = duration * (1 + 0.2 * math.sin(i * 0.5))
        samples = generate_tone(freq, dur, sample_rate)
        all_samples.extend(samples)

    # Add some silence at the end
    all_samples.extend([0.0] * int(0.5 * sample_rate))

    filename = 'fibonacci.wav'
    samples_to_wav(all_samples, filename, sample_rate)

    print(f"Created: {filename}")
    print(f"Duration: {len(all_samples) / sample_rate:.2f}s")
    print(f"Notes derived from: 1, 1, 2, 3, 5, 8, 13, 21, 34...")
    print()
    print("The sequence repeats mod 12 (Pisano period for 12),")
    print("so patterns emerge in the melody.")

if __name__ == "__main__":
    main()
