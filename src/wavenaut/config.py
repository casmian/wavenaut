# src/wavenaut/config.py

# Configuración global del proyecto

SAMPLE_RATE = 44100      # Tasa de muestreo estándar (Hz)
DURATION_DEFAULT = 1.0   # Duración por defecto en segundos
AMPLITUDE_DEFAULT = 0.7  # Amplitud predeterminada (para evitar clipping)

# Límites seguros
MIN_FREQUENCY = 20       # Frecuencia mínima audible (Hz)
MAX_FREQUENCY = 20000    # Frecuencia máxima audible (Hz)
MAX_AMPLITUDE = 1.0      # Nivel máximo de volumen
MAX_DURATION = 60.0     # Máximo tiempo permitido para un sonido (60 segundos)

# Envolvente ADSR por defecto
ADSR_DEFAULT = {
    "attack": 0.1,
    "decay": 0.2,
    "sustain": 0.7,
    "release": 0.3
}

# Otros parámetros útiles
BIT_DEPTH = 16           # Profundidad de bits (opcional por ahora)
NORMALIZE_ON_SAVE = True # Si se normaliza el audio al guardar