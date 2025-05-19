# src/wavenaut/core/sound.py

import numpy as np

from wavenaut.core.wave_generator import (
    generate_sine_wave,
    generate_square_wave,
    generate_triangle_wave,
    generate_sawtooth_wave,
    generate_white_noise
)
from wavenaut.effects.envelope import apply_adsr
from wavenaut.utils.validation import (
    validate_frequency,
    validate_amplitude,
    validate_duration,
    validate_adsr
)


WAVE_TYPES = {
    "sine": generate_sine_wave,
    "square": generate_square_wave,
    "triangle": generate_triangle_wave,
    "sawtooth": generate_sawtooth_wave,
    "noise": generate_white_noise
}


def build_sound(config: dict):
    """
    Construye una onda usando una configuración completa.
    
    Parámetros:
        config (dict): Debe contener:
            - wave_type: tipo de onda ("sine", "square", etc.)
            - freq: frecuencia (Hz)
            - duration: duración en segundos
            - amplitude: amplitud (0.0 - 1.0)
            - adsr: diccionario con attack, decay, sustain, release
    """
    wave_type = config.get("wave_type", "sine")
    freq = config["freq"]
    duration = config["duration"]
    amplitude = config["amplitude"]
    adsr_config = config.get("adsr", {})

    # Validar parámetros antes de generar
    validate_frequency(freq)
    validate_amplitude(amplitude)
    validate_duration(duration)

    # Obtener funciones de generación
    wave_func = WAVE_TYPES.get(wave_type, generate_sine_wave)

    # Generar onda según el tipo
    if wave_type == "noise":
        wave = wave_func(duration=duration, amplitude=amplitude)
    else:
        wave = wave_func(freq=freq, duration=duration, amplitude=amplitude)

    # Aplicar envolvente ADSR si existe
    if adsr_config:
        attack = adsr_config.get("attack", 0.1)
        decay = adsr_config.get("decay", 0.2)
        sustain = adsr_config.get("sustain", 0.7)
        release = adsr_config.get("release", 0.3)

        try:
            validate_adsr(attack, decay, sustain, release, duration)
            wave = apply_adsr(wave, attack=attack, decay=decay, sustain=sustain, release=release)
        except ValueError as e:
            print(f"⚠️ Advertencia: {e}")
            print("ℹ️ Se aplicará una envolvente por defecto.")

    return wave