# src/wavenaut/effects/envelope.py

import numpy as np
from wavenaut.config import SAMPLE_RATE

def apply_adsr(wave: np.ndarray, attack=0.1, decay=0.2, sustain=0.7, release=0.3):
    sr = SAMPLE_RATE
    total_samples = len(wave)

    attack_samples = int(attack * sr)
    decay_samples = int(decay * sr)
    release_samples = int(release * sr)

    # Sustain dura lo que quede después de ataque + decaimiento + release
    sustain_samples = max(0, total_samples - attack_samples - decay_samples - release_samples)

    envelope = np.ones(total_samples)

    # Attack
    if attack_samples > 0:
        envelope[:attack_samples] = np.linspace(0, 1, attack_samples)

    # Decay
    if decay_samples > 0:
        envelope[attack_samples : attack_samples + decay_samples] = np.linspace(
            1, sustain, decay_samples
        )

    # Sustain
    if sustain_samples > 0:
        envelope[attack_samples + decay_samples : attack_samples + decay_samples + sustain_samples] = sustain

    # Release
    if release_samples > 0:
        envelope[-release_samples:] = np.linspace(sustain, 0, release_samples)

    return wave * envelope