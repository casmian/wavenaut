import customtkinter as ctk

class PlaybackControlsFrame(ctk.CTkFrame): 
    def __init__(self, parent, play_current_sound_callback, **kwargs):
        super().__init__(parent, **kwargs)
        
        # This frame is simpler, so a full card look might be too much.
        # Keeping it transparent to blend with MainWindow's background.
        self.configure(fg_color="transparent")

        self.play_current_sound_callback = play_current_sound_callback
        self._create_widgets()

    def _create_widgets(self):
        play_button = ctk.CTkButton(
            self, 
            text="🔊 Play Current Sound", 
            command=self.play_current_sound_callback,
            font=("Roboto", 15, "bold"), # Slightly larger, bold font
            height=36, # Make button a bit taller
            corner_radius=8 # Consistent corner radius
        )
        # Center the button using pack, provide ample padding
        play_button.pack(pady=15, padx=30, fill="x", expand=True) # expand True with fill x centers it if frame is wider
