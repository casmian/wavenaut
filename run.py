import sys
from pathlib import Path

# Añadir 'src/' al PYTHONPATH para cualquier ejecución
project_root = Path(__file__).parent
sys.path.append(str(project_root))
sys.path.append(str(project_root / "src"))

# Ahora puedes importar desde src.wavenaut
import tkinter as tk
from src.wavenaut.ui.cli import iniciar_interfaz_cli
from src.wavenaut.ui.gui.main_window import MainWindow
from src.wavenaut.utils.logger import setup_logger, log_action

setup_logger()
log_action("Programa iniciado")

def menu_principal():
    print("🎵 Bienvenido a wavenaut – Generador procedural de sonidos")
    print("1. Modo CLI")
    print("2. Modo GUI")
    print("3. Salir")

    while True:
        try:
            opcion = int(input("Seleccione una opción: "))
            if opcion == 1:
                print("🔄 Iniciando modo CLI...")
                iniciar_interfaz_cli()
                break
            elif opcion == 2:
                print("🔄 Iniciando modo GUI...")
                root = tk.Tk()
                app = MainWindow(root)
                root.mainloop()
                break
            elif opcion == 3:
                print("👋 ¡Gracias por usar wavenaut!")
                break
            else:
                print("❌ Opción inválida.")
        except ValueError:
            print("❌ Por favor ingrese un número válido.")


if __name__ == "__main__":
    menu_principal()