import numpy as np
import soundfile as sf
from wavenaut.config import SAMPLE_RATE
from pathlib import Path

from typing import Union  # 👈 Añadimos esta línea

# Ruta absoluta relativa al proyecto
OUTPUT_DIR = Path(__file__).parent.parent.parent.parent / "output" / "temp"

def save_wav(wave: Union[list, np.ndarray], filename: str = "output.wav", normalize: bool = True):

    global OUTPUT_DIR
    OUTPUT_DIR.mkdir(exist_ok=True)  # Crea 'output/' si no existe

    wave_np = np.array(wave, dtype=np.float32)

    if normalize:
        max_val = np.max(np.abs(wave_np))
        if max_val > 0:
            wave_np = wave_np / max_val

    full_path = OUTPUT_DIR / filename
    sf.write(full_path, wave_np, SAMPLE_RATE)
    print(f"💾 Archivo guardado: {full_path}")