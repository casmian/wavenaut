# src/wavenaut/audio_engine.py

import sounddevice as sd
import numpy as np


def play_audio(wave: np.ndarray):
    """Reproduce un array de audio usando sounddevice."""
    print("🔊 Reproduciendo...")
    sd.play(wave, samplerate=44100)
    sd.wait()
    print("✅ Reproducción terminada.")