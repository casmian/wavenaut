import customtkinter as ctk
import numpy as np

class WaveformVisualizationFrame(ctk.CTkFrame):
    def __init__(self, parent, sample_rate, **kwargs):
        super().__init__(parent, **kwargs)
        self.sample_rate = sample_rate
        
        # This outer frame will adopt the card style
        self.configure(corner_radius=10, border_width=1)

        frame_title = ctk.CTkLabel(self, text="Waveform Visualization", font=("Roboto", 18, "bold"))
        frame_title.pack(pady=(10,5), padx=15, anchor="w") # Adjusted padding

        self._create_widgets()

    def _create_widgets(self):
        # This inner frame will act as the direct container for the canvas, matching its bg to the canvas
        # It will have a border from the outer frame if the outer frame's fg_color is different.
        # Or, we can give this inner frame a border itself.
        self.canvas_container = ctk.CTkFrame(self, corner_radius=6, border_width=0) # Inner frame for canvas
        self.canvas_container.pack(fill="both", expand=True, padx=10, pady=(5,10))

        appearance_mode = ctk.get_appearance_mode()
        if appearance_mode == "Dark":
            # Use a slightly different shade from the main background for the canvas area if desired
            # Or use the default CTkFrame color which should already be themed.
            canvas_actual_bg_color = self.canvas_container.cget("fg_color") # Get themed color
            self.line_color_default = "#E0E0E0" # Lighter lines on dark canvas
            self.adsr_guide_colors = {"attack": "#F48462", "decay": "#FFCB3D", "release": "#81B29A"} 
            self.text_color = "#DCE4EE" # Light gray text
        else: # Light or System
            canvas_actual_bg_color = self.canvas_container.cget("fg_color")
            self.line_color_default = "#2B2B2B" # Darker lines on light canvas
            self.adsr_guide_colors = {"attack": "#D9534F", "decay": "#F0AD4E", "release": "#5CB85C"}
            self.text_color = "#1E1E1E" # Dark gray text

        import tkinter as tk 
        self.canvas = tk.Canvas(
            self.canvas_container, 
            height=100, # Default height, will expand
            bg=canvas_actual_bg_color, # Match canvas bg to its container's themed bg
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True, padx=0, pady=0) # Canvas fills its CTkFrame container

    def draw_waveform(self, wave: np.ndarray, wave_type: str = "sine", adsr_params: dict = None):
        # Update colors dynamically in case theme changed since __init__
        appearance_mode = ctk.get_appearance_mode()
        if appearance_mode == "Dark":
            canvas_actual_bg_color = self.canvas_container.cget("fg_color")
            self.line_color_default = "#E0E0E0"
            self.adsr_guide_colors = {"attack": "#F48462", "decay": "#FFCB3D", "release": "#81B29A"}
            self.text_color = "#DCE4EE"
        else: # Light or System
            canvas_actual_bg_color = self.canvas_container.cget("fg_color")
            self.line_color_default = "#2B2B2B"
            self.adsr_guide_colors = {"attack": "#D9534F", "decay": "#F0AD4E", "release": "#5CB85C"}
            self.text_color = "#1E1E1E"
        
        self.canvas.configure(bg=canvas_actual_bg_color) # Ensure canvas bg is up-to-date
        self.canvas.delete("all")


        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()

        if w <= 1 or h <= 1: 
            self.after(50, lambda: self.draw_waveform(wave, wave_type, adsr_params))
            return

        if not isinstance(wave, np.ndarray) or len(wave) == 0:
            self.canvas.create_text(
                w / 2, h / 2,
                text="No signal or invalid wave data",
                fill=self.text_color, 
                font=("Roboto", 10)
            )
            return

        mid_y = h // 2
        max_val = np.max(np.abs(wave))
        if max_val == 0: 
            self.canvas.create_line(0, mid_y, w, mid_y, fill=self.line_color_default)
            return

        samples_to_draw = min(len(wave), int(w * 1.5)) 
        indices = np.linspace(0, len(wave) - 1, samples_to_draw, dtype=int)
        wave_preview = wave[indices]
        wave_preview = wave_preview / max_val

        x_scale = w / (len(wave_preview) -1) if len(wave_preview) > 1 else w # Avoid division by zero for single point
        y_scale = mid_y * 0.9  # Use 90% of half-height for amplitude

        coords = []
        for i, val in enumerate(wave_preview):
            x = i * x_scale
            y = mid_y - (val * y_scale)
            coords.append((x, y))

        # Use more vibrant, theme-appropriate colors
        color_map = {
            "sine": "#3498DB",      # Bright Blue
            "square": "#E74C3C",    # Bright Red
            "triangle": "#2ECC71",  # Bright Green
            "sawtooth": "#9B59B6",  # Bright Purple
            "noise": "#95A5A6"      # Greyish
        }
        line_color = color_map.get(wave_type, self.line_color_default)

        if len(coords) > 1:
            self.canvas.create_line(coords, fill=line_color, width=1.5)
        elif coords: # Draw a single point if only one
             x, y = coords[0]
             self.canvas.create_oval(x-1, y-1, x+1, y+1, fill=line_color, outline=line_color)


        if adsr_params:
            try:
                attack_time = adsr_params.get("attack", 0)
                decay_time = adsr_params.get("decay", 0)
                
                total_original_duration_sec = len(wave) / self.sample_rate
                if total_original_duration_sec == 0: return

                adsr_font = ("Roboto", 9, "bold")

                if attack_time > 0:
                    attack_x = (attack_time / total_original_duration_sec) * w
                    if attack_x < w : 
                        self.canvas.create_line(attack_x, 0, attack_x, h, fill=self.adsr_guide_colors["attack"], dash=(4, 2), width=1)
                        self.canvas.create_text(attack_x + 4, 5, text="A", anchor="nw", fill=self.adsr_guide_colors["attack"], font=adsr_font)
                
                if decay_time > 0:
                    decay_x = ((attack_time + decay_time) / total_original_duration_sec) * w
                    if decay_x < w: 
                        self.canvas.create_line(decay_x, 0, decay_x, h, fill=self.adsr_guide_colors["decay"], dash=(4, 2), width=1)
                        self.canvas.create_text(decay_x + 4, 5, text="D", anchor="nw", fill=self.adsr_guide_colors["decay"], font=adsr_font)
            except Exception as e:
                print(f"⚠️ Error drawing ADSR guides: {e}")
