# src/wavenaut/utils/validation.py

from wavenaut.config import MIN_FREQUENCY, MAX_FREQUENCY, MAX_AMPLITUDE, MAX_DURATION


def validate_frequency(freq):
    if not isinstance(freq, (int, float)) or freq <= 0:
        raise ValueError("La frecuencia debe ser un número positivo.")
    if freq < MIN_FREQUENCY:
        raise ValueError(f"La frecuencia debe estar por encima de {MIN_FREQUENCY} Hz (rango audible).")
    if freq > MAX_FREQUENCY:
        raise ValueError(f"La frecuencia no puede superar los {MAX_FREQUENCY} Hz (rango audible).")


def validate_amplitude(amplitude):
    if not isinstance(amplitude, (int, float)) or amplitude < 0 or amplitude > MAX_AMPLITUDE:
        raise ValueError(f"La amplitud debe estar entre 0.0 y {MAX_AMPLITUDE}.")


def validate_duration(duration):
    if not isinstance(duration, (int, float)) or duration <= 0:
        raise ValueError("La duración debe ser un número positivo.")


def validate_adsr(attack, decay, sustain, release, duration):
    total_time = attack + decay + release
    if total_time >= duration:
        raise ValueError(
            f"ADSR demasiado largo: {total_time:.3f}s ≥ {duration:.3f}s. "
            "Reduce Attack/Decay/Release."
        )

    if sustain < 0 or sustain > MAX_AMPLITUDE:
        raise ValueError(f"Sustain debe estar entre 0.0 y {MAX_AMPLITUDE}.")