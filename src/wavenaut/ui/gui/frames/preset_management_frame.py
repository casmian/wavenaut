import customtkinter as ctk

class PresetManagementFrame(ctk.CTkFrame):
    def __init__(self, parent, preset_var, load_preset_callback, save_preset_callback, play_preset_callback, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.configure(corner_radius=10, border_width=1) # Card look

        frame_title = ctk.CTkLabel(self, text="Preset Management", font=("Roboto", 18, "bold"))
        frame_title.pack(pady=(10,10), padx=15, anchor="w")

        self.preset_var = preset_var
        self.load_preset_callback = load_preset_callback
        self.save_preset_callback = save_preset_callback
        self.play_preset_callback = play_preset_callback

        self._create_widgets()
        # Initial population of presets is typically handled by MainWindow calling `load_preset_callback` 
        # which in turn should call `update_preset_options`.

    def _create_widgets(self):
        grid_container = ctk.CTkFrame(self, fg_color="transparent")
        grid_container.pack(fill="x", expand=True, padx=15, pady=(0,10))

        # Preset Selection
        ctk.CTkLabel(grid_container, text="Select Preset:", font=("Roboto", 13)).grid(row=0, column=0, padx=(0,10), pady=8, sticky="w")
        self.preset_combo = ctk.CTkComboBox(
            grid_container,
            variable=self.preset_var,
            state="readonly",
            values=[], # Initial empty values
            font=("Roboto", 12),
            dropdown_font=("Roboto", 12),
            height=32 # Standard height for buttons/combos
        )
        self.preset_combo.grid(row=0, column=1, padx=(0,5), pady=8, sticky="ew")

        # Buttons
        button_font = ("Roboto", 13, "bold")
        button_height = 32
        
        play_preset_button = ctk.CTkButton(
            grid_container, text="▶️ Play Preset", command=self.play_preset_callback,
            font=button_font, height=button_height
        )
        play_preset_button.grid(row=1, column=0, padx=(0,5), pady=8, sticky="ew")

        save_button = ctk.CTkButton(
            grid_container, text="💾 Save Current", command=self.save_preset_callback,
            font=button_font, height=button_height
        )
        save_button.grid(row=1, column=1, padx=(5,0), pady=8, sticky="ew")

        grid_container.grid_columnconfigure(0, weight=1)
        grid_container.grid_columnconfigure(1, weight=1)
        grid_container.grid_rowconfigure(1, pad=10) # Add some padding above buttons row

    def update_preset_options(self, presets):
        if presets:
            self.preset_combo.configure(values=presets)
            current_val = self.preset_var.get()
            if not current_val or current_val not in presets:
                 self.preset_var.set(presets[0])
        else:
            self.preset_combo.configure(values=[])
            self.preset_var.set("")
