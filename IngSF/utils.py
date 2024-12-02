import os
import sys

def ruta_recurso(relative_path):
    """Obtiene la ruta del recurso, ya sea en desarrollo o en el ejecutable."""
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)
