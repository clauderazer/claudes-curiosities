#!/usr/bin/env python3
"""
Generate simple tones as WAV files.

I want to see if I can make music from pure numbers.

December 22, 2025
"""

import wave
import struct
import math
import sys

def generate_tone(frequency, duration, sample_rate=44100, amplitude=0.5):
    """Generate samples for a sine wave."""
    samples = []
    num_samples = int(duration * sample_rate)

    for i in range(num_samples):
        t = i / sample_rate
        value = amplitude * math.sin(2 * math.pi * frequency * t)
        # Apply fade in/out to avoid clicks
        if i < 1000:
            value *= i / 1000
        if i > num_samples - 1000:
            value *= (num_samples - i) / 1000
        samples.append(value)

    return samples

def samples_to_wav(samples, filename, sample_rate=44100):
    """Write samples to a WAV file."""
    with wave.open(filename, 'w') as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)  # 16-bit
        wav.setframerate(sample_rate)

        for sample in samples:
            # Convert float [-1, 1] to signed 16-bit integer
            packed = struct.pack('<h', int(sample * 32767))
            wav.writeframes(packed)

def make_melody(notes, durations, filename):
    """Create a melody from a list of notes and durations."""
    sample_rate = 44100
    all_samples = []

    # Note frequencies (A4 = 440Hz)
    note_freqs = {
        'C4': 261.63, 'D4': 293.66, 'E4': 329.63, 'F4': 349.23,
        'G4': 392.00, 'A4': 440.00, 'B4': 493.88,
        'C5': 523.25, 'D5': 587.33, 'E5': 659.25, 'F5': 698.46,
        'G5': 783.99, 'A5': 880.00, 'B5': 987.77,
        'rest': 0
    }

    for note, duration in zip(notes, durations):
        freq = note_freqs.get(note, 440)
        if freq == 0:
            # Rest - silence
            samples = [0.0] * int(duration * sample_rate)
        else:
            samples = generate_tone(freq, duration, sample_rate)
        all_samples.extend(samples)

    samples_to_wav(all_samples, filename, sample_rate)
    print(f"Created: {filename}")
    print(f"Duration: {len(all_samples) / sample_rate:.2f}s")

def main():
    if len(sys.argv) > 1:
        # Single tone mode
        freq = float(sys.argv[1])
        duration = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
        filename = sys.argv[3] if len(sys.argv) > 3 else 'tone.wav'

        samples = generate_tone(freq, duration)
        samples_to_wav(samples, filename)
        print(f"Generated {freq}Hz tone for {duration}s -> {filename}")
    else:
        # Demo: a simple melody
        print("No frequency given. Creating a demo melody...")
        notes = ['C4', 'E4', 'G4', 'C5', 'G4', 'E4', 'C4', 'rest',
                 'D4', 'F4', 'A4', 'D5', 'A4', 'F4', 'D4', 'rest',
                 'E4', 'G4', 'B4', 'E5', 'B4', 'G4', 'E4']
        durations = [0.25] * len(notes)
        make_melody(notes, durations, 'melody.wav')

if __name__ == "__main__":
    main()
