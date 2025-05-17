import os

# Definimos las carpetas y archivos iniciales
estructura = {
    "src": {
        "core": "__init__.py",
        "ui": "__init__.py",
        "effects": "__init__.py",
        "utils": "__init__.py"
    },
    "assets": None,
    "docs": None,
    "tests": None,
    "README.md": "",
    "LICENSE": "",
    "requirements.txt": ""
}

def crear_estructura(base_dir):
    for carpeta, contenido in estructura.items():
        ruta_carpeta = os.path.join(base_dir, carpeta)
        if isinstance(contenido, dict):  # Si es una carpeta con subcarpetas
            os.makedirs(ruta_carpeta, exist_ok=True)
            for subcarpeta, archivo in contenido.items():
                ruta_sub = os.path.join(ruta_carpeta, subcarpeta)
                os.makedirs(ruta_sub, exist_ok=True)
                if archivo:
                    with open(os.path.join(ruta_sub, archivo), 'w') as f:
                        pass  # Creamos el archivo vacío
        elif contenido is None:  # Carpetas simples
            os.makedirs(ruta_carpeta, exist_ok=True)
        else:  # Archivos sueltos
            with open(ruta_carpeta, 'w') as f:
                f.write(contenido)

if __name__ == "__main__":
    crear_estructura(".")
    print("✅ Estructura de proyecto creada exitosamente.")