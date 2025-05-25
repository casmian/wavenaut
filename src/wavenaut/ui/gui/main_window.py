# src/wavenaut/ui/gui/main_window.py

import customtkinter as ctk
from tkinter import simpledialog # simpledialog is not part of customtkinter, keep as is or find alternative
import numpy as np

# Importar desde la estructura del proyecto
from wavenaut.core.sound import build_sound
from wavenaut.audio_engine import play_audio
from wavenaut.utils.logger import log_action, log_warning
from wavenaut.generators.preset_manager import save_preset, load_preset, PRESETS_DIR

# Import new frames (assuming they will also be updated to CustomTkinter)
from .frames.waveform_controls_frame import WaveformControlsFrame
from .frames.adsr_controls_frame import ADSRControlsFrame
from .frames.preset_management_frame import PresetManagementFrame
from .frames.waveform_visualization_frame import WaveformVisualizationFrame
from .frames.playback_controls_frame import PlaybackControlsFrame

sample_rate = 44100

class MainWindow:
    def __init__(self, root: ctk.CTk): # Type hint for root
        self.root = root
        self.root.title("🎵 wavenaut – Sound Synthesizer") # Slightly more professional title
        self.root.geometry("520x820") # Increased size slightly for more padding

        # Variables de control - CustomTkinter uses its own StringVar, DoubleVar
        self.wave_type_var = ctk.StringVar(value="sine")
        self.freq_var = ctk.DoubleVar(value=440.0)
        self.duration_var = ctk.DoubleVar(value=1.0)
        self.amplitude_var = ctk.DoubleVar(value=0.7)

        self.attack_var = ctk.DoubleVar(value=0.1)
        self.decay_var = ctk.DoubleVar(value=0.2)
        self.sustain_var = ctk.DoubleVar(value=0.7)
        self.release_var = ctk.DoubleVar(value=0.3)
        
        self.preset_var = ctk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        # Main container frame for better padding and organization
        main_frame = ctk.CTkFrame(self.root, fg_color="transparent") # Make main_frame transparent
        main_frame.pack(fill="both", expand=True, padx=15, pady=15) # Increased padding

        # Título
        title_label = ctk.CTkLabel(main_frame, text="🎛️ WaveNaut Sound Synthesizer", font=("Roboto", 26, "bold")) # Changed font
        title_label.pack(pady=(0, 20)) # Increased bottom padding

        # Waveform Controls Frame
        self.waveform_controls_frame = WaveformControlsFrame(
            main_frame,
            self.wave_type_var,
            self.freq_var,
            self.duration_var,
            self.amplitude_var
        )
        self.waveform_controls_frame.pack(pady=(0,10), fill="x", padx=10) # Consistent padding

        # ADSR Controls Frame
        self.adsr_controls_frame = ADSRControlsFrame(
            main_frame,
            self.attack_var,
            self.decay_var,
            self.sustain_var,
            self.release_var
        )
        self.adsr_controls_frame.pack(pady=10, fill="x", padx=10) # Consistent padding

        # Playback Controls Frame (for current sound)
        self.playback_controls_frame = PlaybackControlsFrame(
            main_frame,
            self.reproducir_sonido_actual 
        )
        self.playback_controls_frame.pack(pady=10, fill="x", padx=10)
        
        # Preset Management Frame
        self.preset_management_frame = PresetManagementFrame(
            main_frame,
            self.preset_var,
            self.cargar_presets_disponibles, 
            self.guardar_preset_actual,
            self.reproducir_preset_seleccionado
        )
        self.preset_management_frame.pack(pady=10, fill="x", padx=10)

        # Waveform Visualization Frame
        self.waveform_visualization_frame = WaveformVisualizationFrame(main_frame, sample_rate)
        self.waveform_visualization_frame.pack(pady=10, fill="both", expand=True, padx=10)
        
        # Status Label
        self.status_label = ctk.CTkLabel(main_frame, text="✅ Ready", font=("Roboto", 12)) # Changed font
        self.status_label.pack(pady=(15,0), fill="x") # Increased top padding
        
    def _get_current_adsr_params(self):
        return {
            "attack": self.attack_var.get(),
            "decay": self.decay_var.get(),
            "sustain": self.sustain_var.get(),
            "release": self.release_var.get()
        }

    def _get_current_sound_config(self):
        return {
            "wave_type": self.wave_type_var.get(),
            "freq": self.freq_var.get(),
            "duration": self.duration_var.get(),
            "amplitude": self.amplitude_var.get(),
            "adsr": self._get_current_adsr_params()
        }

    def dibujar_onda_actual(self, wave: np.ndarray, wave_type: str):
        """Helper to draw the current wave with ADSR params."""
        adsr_params = self._get_current_adsr_params()
        self.waveform_visualization_frame.draw_waveform(wave, wave_type, adsr_params)
          
    def reproducir_preset_seleccionado(self):
        """Carga y reproduce el preset seleccionado directamente"""
        nombre = self.preset_var.get()
        if not nombre:
            if not nombre:
                self.status_label.configure(text="⚠️ No preset selected.") # Use .configure for CTk widgets
                log_warning("No preset selected for playback.")
                return

            try:
                preset_data = load_preset(nombre)
                config = preset_data 

                self.wave_type_var.set(config.get("wave_type", "sine"))
                self.freq_var.set(config.get("freq", 440.0))
                self.duration_var.set(config.get("duration", 1.0))
                self.amplitude_var.set(config.get("amplitude", 0.7))
                
                adsr = config.get("adsr", {})
                self.attack_var.set(adsr.get("attack", 0.1))
                self.decay_var.set(adsr.get("decay", 0.2))
                self.sustain_var.set(adsr.get("sustain", 0.7))
                self.release_var.set(adsr.get("release", 0.3))

                log_action(f"Reproduciendo preset '{nombre}': {config}")
                
                wave = build_sound(config)
                self.dibujar_onda_actual(wave, wave_type=config["wave_type"])
                play_audio(wave)
                self.status_label.configure(text=f"🎵 Playing preset: {nombre}")

            except Exception as e:
                log_warning(f"Error al cargar o reproducir el preset '{nombre}': {e}")
                self.status_label.configure(text=f"❌ Error playing preset: {e}")

    def cargar_presets_disponibles(self):
        """Carga los nombres de los presets disponibles en el desplegable del PresetManagementFrame."""
        try:
            presets = sorted([f.stem for f in PRESETS_DIR.glob("*.json") if f.is_file()])
            # Ensure preset_management_frame is initialized before calling methods on it
            if hasattr(self, 'preset_management_frame') and self.preset_management_frame:
                self.preset_management_frame.update_preset_options(presets)
            
            if presets:
                 log_action(f"Presets cargados: {', '.join(presets)}")
            else:
                log_action("No presets found to load.")
        except Exception as e:
            log_warning(f"Error al cargar presets: {e}")
            self.status_label.configure(text="❌ Error loading presets.")
            if hasattr(self, 'preset_management_frame') and self.preset_management_frame:
                self.preset_management_frame.update_preset_options([])

    def guardar_preset_actual(self):
        """Guarda la configuración actual como un nuevo preset."""
        # customtkinter.CTkInputDialog is available for simple string input
        dialog = ctk.CTkInputDialog(text="Enter preset name:", title="Save Preset")
        nombre = dialog.get_input() # This will show the dialog and wait for input

        if not nombre: # User cancelled or entered nothing
            log_action("Guardado de preset cancelado por el usuario.")
            return

        config = self._get_current_sound_config()

        try:
            save_preset(nombre, config)
            log_action(f"Preset '{nombre}' guardado con configuración: {config}")
            self.status_label.configure(text=f"💾 Preset '{nombre}' saved!")
            self.cargar_presets_disponibles()  # Refresh preset list
        except Exception as e:
            log_warning(f"Error al guardar el preset '{nombre}': {e}")
            self.status_label.configure(text=f"❌ Error saving preset: {e}")

    def reproducir_sonido_actual(self):
        """Genera y reproduce el sonido con los parámetros actuales de la UI."""
        config = self._get_current_sound_config()
        log_action(f"Generando sonido con config actual: {config}")
        
        try:
            wave = build_sound(config)
            self.dibujar_onda_actual(wave, wave_type=config["wave_type"])
            play_audio(wave)
            self.status_label.configure(text="✅ Sound generated and played!")
        except ValueError as e: 
            log_warning(f"Error al generar sonido: {e}. Config: {config}")
            self.status_label.configure(text=f"❌ Error: {e}")
        except Exception as e: 
            log_warning(f"Error inesperado al generar sonido: {e}. Config: {config}")
            self.status_label.configure(text=f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    # This block is for direct execution, actual app launch is handled by run.py
    # So, this part should also be updated if direct testing of this file is desired.
    ctk.set_appearance_mode("dark") # "System" or "Light" can also be tested
    ctk.set_default_color_theme("dark-blue") # Try "dark-blue" or "green"
    
    root = ctk.CTk()
    app = MainWindow(root)
    root.mainloop()