# src/wavenaut/core/wave_generator.py

import numpy as np
from wavenaut.config import SAMPLE_RATE, DURATION_DEFAULT, AMPLITUDE_DEFAULT, MAX_AMPLITUDE
from wavenaut.utils.validation import validate_frequency, validate_amplitude


def generate_sine_wave(freq=440.0, duration=None, amplitude=None):
    """
    Genera una onda senoidal con frecuencia, duración y amplitud especificadas.
    """
    validate_frequency(freq)
    amplitude = amplitude or AMPLITUDE_DEFAULT
    validate_amplitude(amplitude)
    duration = duration or DURATION_DEFAULT
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    return amplitude * np.sin(2 * np.pi * freq * t)


def generate_square_wave(freq=440.0, duration=None, amplitude=None):
    validate_frequency(freq)
    amplitude = amplitude or AMPLITUDE_DEFAULT
    validate_amplitude(amplitude)
    duration = duration or DURATION_DEFAULT
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    return amplitude * np.sign(np.sin(2 * np.pi * freq * t))


def generate_triangle_wave(freq=440.0, duration=None, amplitude=None):
    validate_frequency(freq)
    amplitude = amplitude or AMPLITUDE_DEFAULT
    validate_amplitude(amplitude)
    duration = duration or DURATION_DEFAULT
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    return amplitude * (2 * np.abs(2 * (t * freq - np.floor(t * freq + 0.5))) - 1)


def generate_sawtooth_wave(freq=440.0, duration=None, amplitude=None):
    validate_frequency(freq)
    amplitude = amplitude or AMPLITUDE_DEFAULT
    validate_amplitude(amplitude)
    duration = duration or DURATION_DEFAULT
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    return amplitude * (2 * (freq * t - np.floor(freq * t)) - 1)


def generate_white_noise(duration=None, amplitude=None):
    amplitude = amplitude or AMPLITUDE_DEFAULT
    validate_amplitude(amplitude)
    duration = duration or DURATION_DEFAULT
    num_samples = int(SAMPLE_RATE * duration)
    return amplitude * np.random.uniform(-1.0, 1.0, size=num_samples)