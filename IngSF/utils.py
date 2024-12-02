import os
import sys

def ruta_recurso(relative_path):
    """
    Obtiene la ruta del recurso ya sea en desarrollo o cuando se empaqueta el ejecutable.
    :param relative_path: Ruta relativa al archivo
    :return: Ruta absoluta al recurso
    """
    base_path = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    return os.path.join(base_path, relative_path)
