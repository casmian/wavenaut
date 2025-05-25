import customtkinter as ctk

class ADSRControlsFrame(ctk.CTkFrame): 
    def __init__(self, parent, attack_var, decay_var, sustain_var, release_var, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.configure(corner_radius=10, border_width=1) # Card look

        frame_title = ctk.CTkLabel(self, text="ADSR Envelope", font=("Roboto", 18, "bold")) # Updated font
        frame_title.pack(pady=(10,10), padx=15, anchor="w") # Increased padding

        self.attack_var = attack_var
        self.decay_var = decay_var
        self.sustain_var = sustain_var
        self.release_var = release_var

        self._create_widgets()

    def _create_widgets(self):
        grid_container = ctk.CTkFrame(self, fg_color="transparent") # Internal grid transparent
        grid_container.pack(fill="x", expand=True, padx=15, pady=(0,10)) # Add padding

        slider_params = {
            "button_corner_radius": 5,
            "button_length": 15
        }

        # Attack
        ctk.CTkLabel(grid_container, text="Attack (s):", font=("Roboto", 13)).grid(row=0, column=0, sticky="w", padx=(0,10), pady=8)
        attack_slider = ctk.CTkSlider(
            grid_container, from_=0.0, to=2.0, number_of_steps=200, 
            orientation="horizontal", variable=self.attack_var, **slider_params
        )
        attack_slider.grid(row=0, column=1, padx=(0,5), pady=8, sticky="ew")

        # Decay
        ctk.CTkLabel(grid_container, text="Decay (s):", font=("Roboto", 13)).grid(row=1, column=0, sticky="w", padx=(0,10), pady=8)
        decay_slider = ctk.CTkSlider(
            grid_container, from_=0.0, to=2.0, number_of_steps=200,
            orientation="horizontal", variable=self.decay_var, **slider_params
        )
        decay_slider.grid(row=1, column=1, padx=(0,5), pady=8, sticky="ew")

        # Sustain
        ctk.CTkLabel(grid_container, text="Sustain (0-1):", font=("Roboto", 13)).grid(row=2, column=0, sticky="w", padx=(0,10), pady=8)
        sustain_slider = ctk.CTkSlider(
            grid_container, from_=0.0, to=1.0, number_of_steps=100,
            orientation="horizontal", variable=self.sustain_var, **slider_params
        )
        sustain_slider.grid(row=2, column=1, padx=(0,5), pady=8, sticky="ew")

        # Release
        ctk.CTkLabel(grid_container, text="Release (s):", font=("Roboto", 13)).grid(row=3, column=0, sticky="w", padx=(0,10), pady=8)
        release_slider = ctk.CTkSlider(
            grid_container, from_=0.0, to=2.0, number_of_steps=200,
            orientation="horizontal", variable=self.release_var, **slider_params
        )
        release_slider.grid(row=3, column=1, padx=(0,5), pady=8, sticky="ew")

        grid_container.grid_columnconfigure(0, weight=0)
        grid_container.grid_columnconfigure(1, weight=1)
