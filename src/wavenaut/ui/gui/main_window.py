# src/wavenaut/ui/gui/main_window.py

import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
import numpy as np

# Importar desde la estructura del proyecto
from wavenaut.core.sound import build_sound
from wavenaut.audio_engine import play_audio
from wavenaut.utils.logger import log_action, log_warning
from wavenaut.generators.preset_manager import save_preset, load_preset, PRESETS_DIR
sample_rate = 44100

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("🎵 wavenaut – Generador de Sonidos")
        self.root.geometry("450x700")  # Ancho x Alto

        # Variables de control
        self.wave_type_var = tk.StringVar(value="sine")
        self.freq_var = tk.DoubleVar(value=440.0)
        self.duration_var = tk.DoubleVar(value=1.0)
        self.amplitude_var = tk.DoubleVar(value=0.7)

        self.attack_var = tk.DoubleVar(value=0.1)
        self.decay_var = tk.DoubleVar(value=0.2)
        self.sustain_var = tk.DoubleVar(value=0.7)
        self.release_var = tk.DoubleVar(value=0.3)

        # ✅ Definimos preset_var antes de usarlo
        self.preset_var = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        # Título
        title_label = tk.Label(self.root, text="🎛️ Generador de Sonidos", font=("Arial", 16))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Forma de onda
        ttk.Label(self.root, text="Forma de onda").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        wave_combo = ttk.Combobox(
            self.root,
            textvariable=self.wave_type_var,
            values=["sine", "square", "triangle", "sawtooth", "noise"]
        )
        wave_combo.grid(row=1, column=1, padx=10, pady=5)

        # Frecuencia (Hz)
        ttk.Label(self.root, text="Frecuencia (Hz)").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        freq_slider = tk.Scale(
            self.root, from_=20, to=5000, resolution=1,
            orient="horizontal", variable=self.freq_var
        )
        freq_slider.grid(row=2, column=1, padx=10, pady=5)

        # Duración (segundos)
        ttk.Label(self.root, text="Duración (segundos)").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        duration_slider = tk.Scale(
            self.root, from_=0.1, to=5.0, resolution=0.01,
            orient="horizontal", variable=self.duration_var
        )
        duration_slider.grid(row=3, column=1, padx=10, pady=5)

        # Amplitud (0.0 - 1.0)
        ttk.Label(self.root, text="Amplitud (0.0 - 1.0)").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        amplitude_slider = tk.Scale(
            self.root, from_=0.0, to=1.0, resolution=0.01,
            orient="horizontal", variable=self.amplitude_var
        )
        amplitude_slider.grid(row=4, column=1, padx=10, pady=5)

        # Attack
        ttk.Label(self.root, text="Attack").grid(row=5, column=0, sticky="w", padx=10, pady=5)
        attack_slider = tk.Scale(
            self.root, from_=0.0, to=2.0, resolution=0.01,
            orient="horizontal", variable=self.attack_var
        )
        attack_slider.grid(row=5, column=1, padx=10, pady=5)

        # Decay
        ttk.Label(self.root, text="Decay").grid(row=6, column=0, sticky="w", padx=10, pady=5)
        decay_slider = tk.Scale(
            self.root, from_=0.0, to=2.0, resolution=0.01,
            orient="horizontal", variable=self.decay_var
        )
        decay_slider.grid(row=6, column=1, padx=10, pady=5)

        # Sustain
        ttk.Label(self.root, text="Sustain").grid(row=7, column=0, sticky="w", padx=10, pady=5)
        sustain_slider = tk.Scale(
            self.root, from_=0.0, to=1.0, resolution=0.01,
            orient="horizontal", variable=self.sustain_var
        )
        sustain_slider.grid(row=7, column=1, padx=10, pady=5)

        # Release
        ttk.Label(self.root, text="Release").grid(row=8, column=0, sticky="w", padx=10, pady=5)
        release_slider = tk.Scale(
            self.root, from_=0.0, to=2.0, resolution=0.01,
            orient="horizontal", variable=self.release_var
        )
        release_slider.grid(row=8, column=1, padx=10, pady=5)

        # Botón Reproducir sonido actual
        play_button = tk.Button(self.root, text="🔊 Reproducir", command=self.reproducir_sonido)
        play_button.grid(row=9, column=0, columnspan=2, pady=10)

        # Sección Presets
        ttk.Label(self.root, text="📂 Presets").grid(
            row=10, column=0, sticky="w", padx=10, pady=5
        )
        self.preset_combo = ttk.Combobox(
            self.root,
            textvariable=self.preset_var
        )
        self.preset_combo.grid(row=10, column=1, padx=10, pady=5)
        self.cargar_presets()  # Carga inicial de presets

        # Botón para reproducir preset seleccionado
        play_preset_button = tk.Button(
            self.root, text="▶️ Reproducir Preset", command=self.reproducir_preset_seleccionado
        )
        play_preset_button.grid(row=11, column=0, pady=5, padx=(10, 5), sticky="ew")

        # Botón para guardar preset actual
        save_button = tk.Button(
            self.root, text="💾 Guardar Preset", command=self.guardar_preset_actual
        )
        save_button.grid(row=11, column=1, pady=5, padx=(5, 10), sticky="ew")

        # Configurar las columnas para expansión equitativa
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # Área de visualización de onda
        ttk.Label(self.root, text="📈 Visualización de Onda").grid(
            row=12, column=0, columnspan=2, sticky="w", padx=10, pady=(15, 5)
        )
        self.canvas = tk.Canvas(self.root, width=400, height=75, bg="white")
        self.canvas.grid(row=13, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        
        self.status_label = tk.Label(self.root, text="✅ Listo.", fg="green")
        self.status_label.grid(row=15, column=0, columnspan=2, pady=5)

    def dibujar_onda(self, wave: np.ndarray, wave_type: str = "sine"):
        self.canvas.delete("all")

        if not isinstance(wave, np.ndarray) or len(wave) == 0:
            print("❌ Onda inválida para visualizar")
            return

        w = 400
        h = 75
        mid_y = h // 2

        max_val = np.max(np.abs(wave))
        if max_val == 0:
            return

        samples_to_draw = 1000
        wave_preview = wave[:samples_to_draw]
        wave_preview = wave_preview / max_val  # Normalizar entre -1 y 1

        x_scale = w / len(wave_preview)
        y_scale = mid_y * 0.9  # Dejar margen

        coords = []
        for i, val in enumerate(wave_preview):
            x = i * x_scale
            y = mid_y - (val * y_scale)
            coords.append((x, y))

        # Mapeo de color según tipo de onda
        color_map = {
            "sine": "blue",
            "square": "red",
            "triangle": "green",
            "sawtooth": "purple",
            "noise": "gray"
        }
        color = color_map.get(wave_type, "black")

        # Dibujar forma de onda
        for i in range(len(coords) - 1):
            x1, y1 = coords[i]
            x2, y2 = coords[i + 1]
            self.canvas.create_line(x1, y1, x2, y2, fill=color, width=1)

        # Dibujar líneas guía ADSR (si hay configuración válida)
        try:
            attack = self.attack_var.get()
            decay = self.decay_var.get()
            release = self.release_var.get()

            attack_samples = int(attack * sample_rate)
            decay_samples = int(decay * sample_rate)
            release_samples = int(release * sample_rate)

            total_samples = len(wave_preview)

            x_attack_end = (attack_samples / total_samples) * w
            x_decay_end = ((attack_samples + decay_samples) / total_samples) * w
            x_release_start = ((total_samples - release_samples) / total_samples) * w

            # Líneas guía
            self.canvas.create_line(x_attack_end, 0, x_attack_end, h, fill="red", dash=(4, 2), width=1)
            self.canvas.create_line(x_decay_end, 0, x_decay_end, h, fill="orange", dash=(4, 2), width=1)
            self.canvas.create_line(x_release_start, 0, x_release_start, h, fill="blue", dash=(4, 2), width=1)

            # Etiquetas visuales
            self.canvas.create_text(x_attack_end + 5, 10, text="Attack", anchor="nw", fill="red")
            self.canvas.create_text(x_decay_end + 5, 10, text="Decay", anchor="nw", fill="orange")
            self.canvas.create_text(x_release_start + 5, 10, text="Release", anchor="nw", fill="blue")

        except Exception as e:
            print(f"⚠️ No se pudo dibujar la envolvente: {e}")     
          
    def reproducir_preset_seleccionado(self):
        """Carga y reproduce el preset seleccionado directamente"""
        nombre = self.preset_var.get()
        if not nombre:
            print("❌ No se ha seleccionado un preset.")
            return

        try:
            preset_data = load_preset(nombre)

            config = {
                "wave_type": preset_data.get("wave_type", "sine"),
                "freq": preset_data.get("freq", 440.0),
                "duration": preset_data.get("duration", 1.0),
                "amplitude": preset_data.get("amplitude", 0.7),
                "adsr": preset_data.get("adsr", {
                    "attack": 0.1,
                    "decay": 0.2,
                    "sustain": 0.7,
                    "release": 0.3
                })
            }

            print(f"🎧 Reproduciendo preset '{nombre}' con configuración:")
            for k, v in config.items():
                print(f"  {k}: {v}")

            wave = build_sound(config)
            self.dibujar_onda(wave, wave_type=config["wave_type"])
            play_audio(wave)

        except Exception as e:
            print(f"❌ Error al cargar o reproducir el preset: {e}")

    def cargar_presets(self):
        """Carga los nombres de los presets disponibles en el desplegable"""
        try:
            presets = [f.stem for f in PRESETS_DIR.glob("*.json")]
            self.preset_combo["values"] = presets
            if presets:
                self.preset_var.set(presets[0])
        except Exception as e:
            print(f"❌ Error al cargar presets: {e}")

    def guardar_preset_actual(self):
        """Guarda la configuración actual como preset"""
        nombre = simpledialog.askstring("Guardar Preset", "Nombre del preset:")
        if not nombre:
            return

        config = {
            "wave_type": self.wave_type_var.get(),
            "freq": self.freq_var.get(),
            "duration": self.duration_var.get(),
            "amplitude": self.amplitude_var.get(),
            "adsr": {
                "attack": self.attack_var.get(),
                "decay": self.decay_var.get(),
                "sustain": self.sustain_var.get(),
                "release": self.release_var.get()
            }
        }

        save_preset(nombre, config)
        self.cargar_presets()  # Refrescar lista

    def reproducir_sonido(self):
        """Genera y reproduce el sonido con los parámetros actuales"""
        config = {
            "wave_type": self.wave_type_var.get(),
            "freq": self.freq_var.get(),
            "duration": self.duration_var.get(),
            "amplitude": self.amplitude_var.get(),
            "adsr": {
                "attack": self.attack_var.get(),
                "decay": self.decay_var.get(),
                "sustain": self.sustain_var.get(),
                "release": self.release_var.get()
            }
        }

        log_action(f"Usuario generó sonido: {config}")
        
        try:
            wave = build_sound(config)
            self.dibujar_onda(wave, wave_type=config["wave_type"])
            play_audio(wave)
            self.status_label.config(text="✅ Sonido generado correctamente.", fg="green")
        except ValueError as e:
            print(f"❌ Error al generar sonido: {e}")
            self.status_label.config(text=f"❌ {e}", fg="red")


if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()