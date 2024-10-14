# main.py
import sys
from PyQt5.QtWidgets import QApplication
from Ventanas.inicio_sesion import VentanaInicio

#def cargar_estilos():
 #   with open("Recursos/estilos.qss", "r") as f:
  #      estilos = f.read()
   # return estilos

if __name__ == '__main__':
    app = QApplication(sys.argv)
    #app.setStyleSheet(cargar_estilos())  # Aplicar el estilo QSS
    ventana_inicio = VentanaInicio()
    ventana_inicio.show()
    sys.exit(app.exec_())
