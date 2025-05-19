# src/wavenaut/generators/preset_manager.py

import json
from pathlib import Path
from typing import Dict, Union

# Ruta base para presets
PRESETS_DIR = Path(__file__).parent.parent.parent.parent / "presets" / "default"


def save_preset(name: str, data: dict):
    """
    Guarda una configuración como preset en formato JSON.
    
    Parámetros:
    - name (str): Nombre del preset (se usará como nombre del archivo).
    - data (dict): Diccionario con la configuración del sonido.
    """
    preset_path = PRESETS_DIR / f"{name}.json"
    with open(preset_path, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"💾 Preset '{name}' guardado en {preset_path}")


def load_preset(name: str) -> Dict[str, Union[int, float, str]]:
    """
    Carga un preset desde su nombre (sin .json).
    
    Retorna:
    - dict: Configuración cargada
    """
    preset_path = PRESETS_DIR / f"{name}.json"
    if not preset_path.exists():
        raise FileNotFoundError(f"No se encontró el preset '{name}'")
    
    with open(preset_path, 'r') as f:
        return json.load(f)