# src/wavenaut/utils/logger.py

import logging
from pathlib import Path

# Ruta actual del archivo
current_path = Path(__file__)

# Salimos 3 veces para llegar a 'src/wavenaut/'
project_root = current_path.parent.parent.parent.parent


# Creamos LOG_DIR de forma más clara
LOG_DIR = project_root / "logs"
LOG_FILE = LOG_DIR / "user_actions.log"

# Aseguramos que exista la carpeta
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Configurar el logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s: %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def setup_logger():
    LOG_DIR.mkdir(exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s: %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE, encoding='utf-8'),
            logging.StreamHandler()  # Para ver logs en consola también
        ]
    )

def log_action(message: str):
    """Escribe una acción del usuario en el log"""
    logging.info(message)

def log_warning(message: str):
    """Escribe una advertencia en el log"""
    logging.warning(message)

def log_error(message: str):
    """Escribe un error en el log"""
    logging.error(message)