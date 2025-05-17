import sounddevice as sd
import numpy as np

# Parámetros básicos
sample_rate = 44100  # Hz
duration = 2         # segundos
frequency = 440      # Hz (nota La)
amplitude = 0.5      # entre 0 y 1

# Generar una onda sinusoidal
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
samples = amplitude * np.sin(2 * np.pi * frequency * t)

# Reproducir
print("🔊 Reproduciendo...")
sd.play(samples, samplerate=sample_rate)
sd.wait()  # Espera hasta que termine de reproducirse
print("✅ Fin.")