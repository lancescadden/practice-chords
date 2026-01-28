"""Audio playback for chord sounds and metronome."""

import threading
import time
from typing import Callable

# Audio availability flag
AUDIO_AVAILABLE = False

try:
    import numpy as np
    import sounddevice as sd
    AUDIO_AVAILABLE = True
except ImportError:
    np = None
    sd = None


# Guitar string frequencies (E2 to e4)
STRING_FREQS = {
    'E': 82.41,   # Low E
    'A': 110.00,
    'D': 146.83,
    'G': 196.00,
    'B': 246.94,
    'e': 329.63,  # High e
}

# Fret multiplier (12-TET)
FRET_RATIO = 2 ** (1/12)


def get_note_freq(string: str, fret: int) -> float:
    """Calculate frequency for a note on a specific string and fret."""
    base_freq = STRING_FREQS[string]
    return base_freq * (FRET_RATIO ** fret)


def generate_pluck(freq: float, duration: float = 1.5, sample_rate: int = 44100) -> 'np.ndarray':
    """Generate a plucked string sound using Karplus-Strong algorithm."""
    if not AUDIO_AVAILABLE:
        return None

    # Simplified Karplus-Strong synthesis
    n_samples = int(duration * sample_rate)
    period = int(sample_rate / freq)

    # Initialize with noise burst
    buffer = np.random.uniform(-1, 1, period).astype(np.float32)

    # Output array
    output = np.zeros(n_samples, dtype=np.float32)

    # Karplus-Strong loop
    for i in range(n_samples):
        output[i] = buffer[i % period]
        # Low-pass filter (averaging)
        buffer[i % period] = 0.996 * 0.5 * (buffer[i % period] + buffer[(i + 1) % period])

    # Apply envelope
    envelope = np.exp(-3 * np.linspace(0, 1, n_samples))
    output *= envelope

    return output


def play_chord(frets: tuple[int | None, ...], strum_delay: float = 0.03):
    """Play a chord by strumming all strings."""
    if not AUDIO_AVAILABLE:
        return

    strings = ['E', 'A', 'D', 'G', 'B', 'e']
    sample_rate = 44100
    duration = 2.0

    # Generate samples for each string
    samples = []
    for i, (string, fret) in enumerate(zip(strings, frets)):
        if fret is None:
            continue
        freq = get_note_freq(string, fret)
        wave = generate_pluck(freq, duration, sample_rate)
        # Stagger the start times
        delay_samples = int(i * strum_delay * sample_rate)
        padded = np.zeros(len(wave) + delay_samples, dtype=np.float32)
        padded[delay_samples:] = wave
        samples.append(padded)

    if not samples:
        return

    # Mix all strings
    max_len = max(len(s) for s in samples)
    mixed = np.zeros(max_len, dtype=np.float32)
    for s in samples:
        mixed[:len(s)] += s

    # Normalize
    mixed = mixed / (np.max(np.abs(mixed)) + 0.001) * 0.7

    # Play
    try:
        sd.play(mixed, sample_rate)
    except Exception:
        pass


def play_click(freq: float = 1000, duration: float = 0.05):
    """Play a metronome click."""
    if not AUDIO_AVAILABLE:
        return

    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), dtype=np.float32)
    wave = np.sin(2 * np.pi * freq * t)
    envelope = np.exp(-30 * t)
    wave *= envelope * 0.5

    try:
        sd.play(wave, sample_rate)
    except Exception:
        pass


class Metronome:
    """Background metronome with configurable BPM."""

    def __init__(self, bpm: int = 80):
        self.bpm = bpm
        self._running = False
        self._thread: threading.Thread | None = None
        self._beat_callback: Callable[[], None] | None = None

    def start(self, beat_callback: Callable[[], None] | None = None):
        """Start the metronome."""
        if self._running:
            return

        self._running = True
        self._beat_callback = beat_callback
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self):
        """Stop the metronome."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=0.5)
            self._thread = None

    def set_bpm(self, bpm: int):
        """Change the tempo."""
        self.bpm = max(40, min(200, bpm))

    def _run(self):
        """Metronome loop."""
        beat = 0
        while self._running:
            # Accent on beat 1
            freq = 1200 if beat == 0 else 800
            play_click(freq)

            if self._beat_callback:
                self._beat_callback()

            beat = (beat + 1) % 4
            time.sleep(60.0 / self.bpm)

    @property
    def is_running(self) -> bool:
        return self._running


def stop_all():
    """Stop all playing audio."""
    if AUDIO_AVAILABLE:
        try:
            sd.stop()
        except Exception:
            pass
