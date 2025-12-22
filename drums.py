#!/usr/bin/env python3
"""
drums.py - Simple drum machine using synthesized sounds.

Generates kick, snare, and hi-hat sounds from sine waves
and noise, then plays patterns through the speakers.

Requires: pyaudio or simpleaudio (falls back to file output)
"""

import math
import random
import struct
import sys
import wave

SAMPLE_RATE = 44100
CHANNELS = 1
BITS = 16


def generate_kick(duration: float = 0.2) -> bytes:
    """Generate a kick drum sound - low frequency with pitch decay."""
    samples = []
    n_samples = int(SAMPLE_RATE * duration)

    for i in range(n_samples):
        t = i / SAMPLE_RATE
        # Pitch envelope: starts high, drops to low
        freq = 150 * math.exp(-20 * t) + 50
        # Amplitude envelope: sharp attack, gradual decay
        amp = math.exp(-8 * t)
        # Sine wave at decaying frequency
        sample = amp * math.sin(2 * math.pi * freq * t)
        samples.append(int(sample * 32767 * 0.8))

    return struct.pack(f'{len(samples)}h', *samples)


def generate_snare(duration: float = 0.15) -> bytes:
    """Generate a snare sound - noise + tone."""
    samples = []
    n_samples = int(SAMPLE_RATE * duration)

    for i in range(n_samples):
        t = i / SAMPLE_RATE
        # Amplitude envelope
        amp = math.exp(-15 * t)
        # Mix of tone (200Hz) and noise
        tone = 0.4 * math.sin(2 * math.pi * 200 * t)
        noise = 0.6 * (random.random() * 2 - 1)
        sample = amp * (tone + noise)
        samples.append(int(sample * 32767 * 0.7))

    return struct.pack(f'{len(samples)}h', *samples)


def generate_hihat(duration: float = 0.05) -> bytes:
    """Generate a hi-hat sound - high frequency noise."""
    samples = []
    n_samples = int(SAMPLE_RATE * duration)

    for i in range(n_samples):
        t = i / SAMPLE_RATE
        # Very fast decay
        amp = math.exp(-40 * t)
        # Filtered noise (band-pass effect via mixing)
        noise = random.random() * 2 - 1
        # High frequency component
        hf = 0.5 * math.sin(2 * math.pi * 8000 * t + random.random())
        sample = amp * (noise * 0.7 + hf * 0.3)
        samples.append(int(sample * 32767 * 0.5))

    return struct.pack(f'{len(samples)}h', *samples)


def silence(duration: float) -> bytes:
    """Generate silence."""
    n_samples = int(SAMPLE_RATE * duration)
    return struct.pack(f'{n_samples}h', *([0] * n_samples))


def mix_at_position(buffer: bytearray, sound: bytes, position: int):
    """Mix a sound into the buffer at a given sample position."""
    # Convert to list of samples
    sound_samples = struct.unpack(f'{len(sound)//2}h', sound)
    byte_pos = position * 2

    for i, sample in enumerate(sound_samples):
        if byte_pos + i * 2 + 1 >= len(buffer):
            break
        # Get existing sample
        existing = struct.unpack_from('h', buffer, byte_pos + i * 2)[0]
        # Mix (with clipping)
        mixed = max(-32768, min(32767, existing + sample))
        struct.pack_into('h', buffer, byte_pos + i * 2, mixed)


def generate_pattern(pattern: str, bpm: float = 120) -> bytes:
    """
    Generate audio from a pattern string.

    Pattern format: each character is a 16th note
    K = kick, S = snare, H = hi-hat, . = rest
    Multiple can play at once: KH = kick + hi-hat

    Example: "K...S..HK..HS..H" = classic rock beat
    """
    beat_duration = 60.0 / bpm
    sixteenth = beat_duration / 4

    # Calculate total duration
    total_duration = len(pattern) * sixteenth
    total_samples = int(SAMPLE_RATE * total_duration)

    # Create buffer
    buffer = bytearray(total_samples * 2)

    # Pre-generate sounds
    kick = generate_kick()
    snare = generate_snare()
    hihat = generate_hihat()

    # Place sounds
    for i, char in enumerate(pattern):
        position = int(i * sixteenth * SAMPLE_RATE)
        if 'K' in char or 'k' in char:
            mix_at_position(buffer, kick, position)
        if 'S' in char or 's' in char:
            mix_at_position(buffer, snare, position)
        if 'H' in char or 'h' in char:
            mix_at_position(buffer, hihat, position)

    return bytes(buffer)


def save_wav(filename: str, audio: bytes):
    """Save audio to a WAV file."""
    with wave.open(filename, 'wb') as f:
        f.setnchannels(CHANNELS)
        f.setsampwidth(BITS // 8)
        f.setframerate(SAMPLE_RATE)
        f.writeframes(audio)


def play_audio(audio: bytes):
    """Try to play audio through speakers."""
    try:
        import simpleaudio as sa
        play_obj = sa.play_buffer(audio, CHANNELS, BITS // 8, SAMPLE_RATE)
        play_obj.wait_done()
        return True
    except ImportError:
        pass

    try:
        import pyaudio
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(BITS // 8),
                        channels=CHANNELS,
                        rate=SAMPLE_RATE,
                        output=True)
        stream.write(audio)
        stream.stop_stream()
        stream.close()
        p.terminate()
        return True
    except ImportError:
        pass

    return False


# Classic patterns
PATTERNS = {
    "rock": "K..HK..HS..HK..H" * 4,
    "hiphop": "K...K...S...K..." * 4,
    "house": "K.H.K.H.K.H.K.H." * 4,
    "breakbeat": "K..HK.H.S.H.K.H." * 4,
    "random": lambda: ''.join(random.choice(['K', 'S', 'H', '.', '.']) for _ in range(64)),
}


def main():
    if len(sys.argv) > 1:
        pattern_name = sys.argv[1]
    else:
        pattern_name = "rock"

    if pattern_name in PATTERNS:
        pattern = PATTERNS[pattern_name]
        if callable(pattern):
            pattern = pattern()
        print(f"Pattern: {pattern_name}")
    else:
        pattern = pattern_name
        print(f"Custom pattern")

    print(f"Generating: {pattern}")
    audio = generate_pattern(pattern, bpm=120)

    # Try to play, fall back to file
    if play_audio(audio):
        print("Playing...")
    else:
        filename = "/tmp/drums.wav"
        save_wav(filename, audio)
        print(f"Audio libraries not found. Saved to: {filename}")
        print("Install simpleaudio or pyaudio to play directly.")


if __name__ == '__main__':
    main()
