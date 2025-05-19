# src/wavenaut/ui/cli.py

from wavenaut.core.wave_generator import (
    generate_sine_wave,
    generate_square_wave,
    generate_triangle_wave,
    generate_sawtooth_wave,
    generate_white_noise
)
from wavenaut.effects.envelope import apply_adsr
from wavenaut.audio_engine import play_audio
from wavenaut.utils.file_utils import save_wav
from wavenaut.generators.preset_manager import save_preset, load_preset, PRESETS_DIR
from wavenaut.core.sound import build_sound
from typing import Union, Dict
import numpy as np
from pathlib import Path

# -------------------------------
# Funciones auxiliares
# -------------------------------

def mostrar_menu():
    print("\n🎵 Menú de Generación de Sonido")
    print("1. Seleccionar forma de onda")
    print("2. Cargar preset")
    print("3. Salir")

def mostrar_formas_de_onda():
    print("\n🔢 Formas de onda disponibles:")
    print("1. Onda Senoidal")
    print("2. Onda Cuadrada")
    print("3. Onda Triangular")
    print("4. Onda Diente de Sierra")
    print("5. Ruido Blanco")

def obtener_opcion_menu() -> int:
    while True:
        try:
            opcion = int(input("Seleccione una opción: "))
            if 1 <= opcion <= 3:
                return opcion
            else:
                print("❌ Opción fuera de rango.")
        except ValueError:
            print("❌ Por favor ingrese un número válido.")

def obtener_forma_de_onda() -> int:
    mostrar_formas_de_onda()
    while True:
        try:
            forma = int(input("Seleccione la forma de onda (1-5): "))
            if 1 <= forma <= 5:
                return forma
            else:
                print("❌ Selección inválida.")
        except ValueError:
            print("❌ Ingrese un número válido.")

def obtener_parametros(forma: int) -> dict:
    print("\n🎛️  Ajuste los parámetros del sonido:")
    freq = float(input("Ingrese la frecuencia (Hz) [por defecto 440]: ") or "440")
    duration = float(input("Ingrese la duración (segundos) [por defecto 1.0]: ") or "1.0")
    amplitude = float(input("Ingrese la amplitud (0.0 - 1.0) [por defecto 0.7]: ") or "0.7")

    usar_adsr = input("¿Aplicar envolvente ADSR? (s/n): ").lower() == 's'
    attack = decay = sustain = release = None

    if usar_adsr:
        attack = float(input("Attack (segundos) [0.1]: ") or "0.1")
        decay = float(input("Decay (segundos) [0.2]: ") or "0.2")
        sustain = float(input("Sustain (nivel 0.0 - 1.0) [0.7]: ") or "0.7")
        release = float(input("Release (segundos) [0.3]: ") or "0.3")

    guardar = input("¿Guardar esta configuración como preset? (s/n): ").lower() == 's'
    if guardar:
        nombre_preset = input("Nombre del preset (ej: dragon_roar): ")
        wave_types = ["sine", "square", "triangle", "sawtooth", "noise"]
        preset_data = {
            "wave_type": wave_types[forma - 1],
            "freq": freq,
            "duration": duration,
            "amplitude": amplitude,
            "adsr": {
                "attack": attack,
                "decay": decay,
                "sustain": sustain,
                "release": release
            }
        }
        save_preset(nombre_preset, preset_data)

    return {
        "freq": freq,
        "duration": duration,
        "amplitude": amplitude,
        "adsr": {
            "attack": attack,
            "decay": decay,
            "sustain": sustain,
            "release": release
        }
    }

def aplicar_envolvente(wave: Union[list, np.ndarray], adsr: dict):
    return apply_adsr(
        wave,
        attack=adsr["attack"],
        decay=adsr["decay"],
        sustain=adsr["sustain"],
        release=adsr["release"]
    )

def generar_y_reproducir(forma: int, params: dict, preset_data: dict = None):
    if preset_data:
        # Usar todo desde el preset
        wave = build_sound(preset_data)
    else:
        # Generar desde parámetros manuales
        wave_types = ["sine", "square", "triangle", "sawtooth", "noise"]
        wave_type = wave_types[forma - 1]
        wave_config = {
            "wave_type": wave_type,
            "freq": params["freq"],
            "duration": params["duration"],
            "amplitude": params["amplitude"],
            "adsr": params["adsr"]
        }
        wave = build_sound(wave_config)

    play_audio(wave)

    guardar = input("¿Guardar sonido como .wav? (s/n): ").lower() == 's'
    if guardar:
        nombre = input("Nombre del archivo (sin extensión): ")
        save_wav(wave, f"{nombre}.wav")

def cargar_y_usar_preset():
    print("\n📂 Presets disponibles:")
    presets = [f.stem for f in Path(PRESETS_DIR).glob("*.json")]
    if not presets:
        print("⚠️ No hay presets guardados aún.")
        return

    for i, name in enumerate(presets, 1):
        print(f"{i}. {name}")
    try:
        seleccion = int(input("Elija un preset por número: ")) - 1
        preset_name = presets[seleccion]
        preset_data = load_preset(preset_name)

        print(f"\n🎛️  Usando preset '{preset_name}':")
        for k, v in preset_data.items():
            print(f" - {k}: {v}")

        forma_map = {
            "sine": 1,
            "square": 2,
            "triangle": 3,
            "sawtooth": 4,
            "noise": 5
        }

        forma = forma_map.get(preset_data.get("wave_type", "sine"), 1)
        params = {
            "freq": preset_data.get("freq", 440),
            "duration": preset_data.get("duration", 1.0),
            "amplitude": preset_data.get("amplitude", 0.7),
            "adsr": preset_data.get("adsr", {"attack": 0.1, "decay": 0.2, "sustain": 0.7, "release": 0.3})
        }

        generar_y_reproducir(forma, params)

    except IndexError:
        print("❌ Número de preset inválido.")
    except Exception as e:
        print(f"❌ Error al cargar el preset: {e}")

def iniciar_interfaz_cli():
    print("🎵 Bienvenido a wavenaut – Generador procedural de sonidos")
    while True:
        mostrar_menu()
        opcion = obtener_opcion_menu()

        if opcion == 3:
            print("👋 ¡Gracias por usar wavenaut!")
            break

        elif opcion == 1:
            forma = obtener_forma_de_onda()
            params = obtener_parametros(forma)
            generar_y_reproducir(forma, params)

        elif opcion == 2:
            cargar_y_usar_preset()