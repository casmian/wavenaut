import customtkinter as ctk

class WaveformControlsFrame(ctk.CTkFrame): 
    def __init__(self, parent, wave_type_var, freq_var, duration_var, amplitude_var, **kwargs):
        super().__init__(parent, **kwargs)
        
        # Use a default fg_color from the theme, or specify one if needed for card look
        # e.g. self.configure(fg_color=self._apply_appearance_mode(ctk.ThemeManager.theme["CTkFrame"]["fg_color"]))
        # For simplicity, let CTkFrame use its default, or set a specific one like "gray20" for dark mode.
        # If MainWindow's main_frame is transparent, this frame will create the "card"
        self.configure(corner_radius=10, border_width=1) # Add rounded corners and a border for card look

        frame_title = ctk.CTkLabel(self, text="Waveform Shaping", font=("Roboto", 18, "bold")) # Updated font
        frame_title.pack(pady=(10,10), padx=15, anchor="w") # Increased padding

        self.wave_type_var = wave_type_var
        self.freq_var = freq_var
        self.duration_var = duration_var
        self.amplitude_var = amplitude_var

        self._create_widgets()

    def _create_widgets(self):
        grid_container = ctk.CTkFrame(self, fg_color="transparent") # Internal grid should be transparent
        grid_container.pack(fill="x", expand=True, padx=15, pady=(0,10)) # Add padding

        # Waveform Type
        ctk.CTkLabel(grid_container, text="Type:", font=("Roboto", 13)).grid(row=0, column=0, sticky="w", padx=(0,10), pady=8)
        wave_combo = ctk.CTkComboBox(
            grid_container,
            variable=self.wave_type_var, 
            values=["sine", "square", "triangle", "sawtooth", "noise"],
            state="readonly",
            font=("Roboto", 12),
            dropdown_font=("Roboto", 12)
        )
        wave_combo.grid(row=0, column=1, padx=(0,5), pady=8, sticky="ew")

        # Frequency (Hz)
        ctk.CTkLabel(grid_container, text="Frequency (Hz):", font=("Roboto", 13)).grid(row=1, column=0, sticky="w", padx=(0,10), pady=8)
        freq_slider = ctk.CTkSlider(
            grid_container, from_=20, to=5000, number_of_steps=4980, 
            orientation="horizontal", variable=self.freq_var,
            button_corner_radius=5, button_length=15 # Smaller button for slider
        )
        freq_slider.grid(row=1, column=1, padx=(0,5), pady=8, sticky="ew")
        # TODO: Consider adding a CTkEntry or CTkLabel to display the slider's current value numerically.

        # Duration (seconds)
        ctk.CTkLabel(grid_container, text="Duration (s):", font=("Roboto", 13)).grid(row=2, column=0, sticky="w", padx=(0,10), pady=8)
        duration_slider = ctk.CTkSlider(
            grid_container, from_=0.1, to=5.0, number_of_steps=490, 
            orientation="horizontal", variable=self.duration_var,
            button_corner_radius=5, button_length=15
        )
        duration_slider.grid(row=2, column=1, padx=(0,5), pady=8, sticky="ew")

        # Amplitude (0.0 - 1.0)
        ctk.CTkLabel(grid_container, text="Amplitude:", font=("Roboto", 13)).grid(row=3, column=0, sticky="w", padx=(0,10), pady=8)
        amplitude_slider = ctk.CTkSlider(
            grid_container, from_=0.0, to=1.0, number_of_steps=100, 
            orientation="horizontal", variable=self.amplitude_var,
            button_corner_radius=5, button_length=15
        )
        amplitude_slider.grid(row=3, column=1, padx=(0,5), pady=8, sticky="ew")

        grid_container.grid_columnconfigure(0, weight=0) 
        grid_container.grid_columnconfigure(1, weight=1)
