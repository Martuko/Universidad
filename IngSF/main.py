# main.py
import sys
from PyQt5.QtWidgets import QApplication
from Ventanas.inicio_sesion import VentanaInicio

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana_inicio = VentanaInicio()
    ventana_inicio.show()
    sys.exit(app.exec_())
