import os
from pathlib import Path

# Estructura del proyecto
# Estos estan vacios tambein README.md, LICENSE, y requirements.txt.

estructura = {
    "src": {
        "wavenaut": {
            "__init__.py": "",
            "config.py": "",
            "main.py": "",
            "audio_engine.py": "",
            "core": {
                "__init__.py": "",
                "wave_generator.py": ""
            },
            "effects": {
                "__init__.py": "",
                "envelope.py": "",
                "filters.py": "",
                "delay.py": ""
            },
            "utils": {
                "__init__.py": "",
                "file_utils.py": "",
                "validation.py": "",
                "logger.py": ""
            },
            "generators": {
                "__init__.py": "",
                "sfx_generator.py": "",
                "music_generator.py": ""
            },
            "ui": {
                "__init__.py": "",
                "cli.py": "",
                "gui": {
                    "__init__.py": "",
                    "main_window.py": "",
                    "components": {
                        "__init__.py": "",
                        "waveform_controls.py": "",
                        "adsr_editor.py": "",
                        "preset_browser.py": ""
                    }
                }
            }
        }
    },
    "assets": None,  # Esto se creará como un directorio vacío
    "docs": None,    # Esto se creará como un directorio vacío
    "tests": None,   # Esto se creará como un directorio vacío
    "presets": {
        "default": {},  # Directorio vacío
        "community": {} # Directorio vacío
    },
    "run.py": "",
    "README.md": "",
    "LICENSE": "",
    "requirements.txt": ""
}

# Función recursiva para crear directorios y archivos
def crear_estructura_recursiva(directorio_base, elementos_estructura):
    """
    Crea directorios y archivos basado en un diccionario de estructura.

    :param directorio_base: Objeto Path para el directorio actual donde se crearán los elementos.
    :param elementos_estructura: Diccionario que define la estructura.
                                 Las claves son nombres de archivo/directorio.
                                 Los valores pueden ser:
                                 - un diccionario: para un subdirectorio (puede estar vacío).
                                 - una cadena: para un archivo (el contenido de la cadena).
                                 - None: para un directorio vacío explícito.
    """
    for nombre, contenido in elementos_estructura.items():
        # Construir la ruta completa para el elemento actual
        ruta_elemento_actual = directorio_base / nombre

        if isinstance(contenido, dict):
            # Es un directorio
            ruta_elemento_actual.mkdir(parents=True, exist_ok=True)
            # Llamada recursiva para procesar el contenido de este directorio
            # Solo se llama recursivamente si el diccionario no está vacío.
            # Si está vacío (ej. "default": {}), solo se crea el directorio.
            if contenido: 
                crear_estructura_recursiva(ruta_elemento_actual, contenido)
        elif isinstance(contenido, str):
            # Es un archivo
            # Asegurar que el directorio base exista (importante si es un archivo en la raíz)
            directorio_base.mkdir(parents=True, exist_ok=True)
            with open(ruta_elemento_actual, 'w', encoding='utf-8') as f:
                f.write(contenido)
        elif contenido is None:
            # Es un directorio vacío explícito (ej. "assets": None)
            ruta_elemento_actual.mkdir(parents=True, exist_ok=True)
        else:
            # Tipo de contenido no esperado, se podría registrar un aviso o error
            print(f"Advertencia: Tipo de contenido no reconocido para '{nombre}': {type(contenido)}")

if __name__ == "__main__":
    # Directorio raíz donde se creará la estructura del proyecto.
    # Usamos Path(".") para referirnos al directorio actual donde se ejecuta el script.
    directorio_raiz_proyecto = Path(".")
    
    print(f"Creando estructura del proyecto en: {directorio_raiz_proyecto.resolve()}")
    crear_estructura_recursiva(directorio_raiz_proyecto, estructura)
    print("✅ Estructura del proyecto creada exitosamente.")
    print("   El resto de los archivos .py y otros están vacíos según la definición.")
