# main.py
import sys
import os

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QStackedWidget, QLabel, QHBoxLayout
from PyQt5.QtCore import QFile, QTextStream

from Ventanas.inicio_sesion import VentanaInicio
from Ventanas.caja import VentanaCaja
from Ventanas.administrador import VentanaAdministrador
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Inventario")
        self.setGeometry(100, 100, 800, 600)

        # Contenedor principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal (menú lateral + vistas dinámicas)
        main_layout = QHBoxLayout(central_widget)

        # Menú lateral
        

        # Conectar botones del menú
        

        # Agregar el menú lateral al layout principal

        # Vistas dinámicas
        self.stack = QStackedWidget()
        main_layout.addWidget(self.stack)

        # Agregar vistas al stack
        self.vista_inicio = VentanaInicio()
        self.vista_caja = VentanaCaja(usuario=(1, "admin"), sucursal_id=1)  # Ejemplo de usuario y sucursal
        self.vista_administrador = VentanaAdministrador(usuario=(1, "admin"), sucursal_id=1)

        self.stack.addWidget(self.vista_inicio)
        self.stack.addWidget(self.vista_caja)
        self.stack.addWidget(self.vista_administrador)

    def cambiar_vista(self, index):
        self.stack.setCurrentIndex(index)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Cargar el archivo de estilos
    style_file = QFile(os.path.join(BASE_DIR, "Recursos/styles.qss"))
    if style_file.open(QFile.ReadOnly | QFile.Text):
        print("Styles cargados exitosamente")
        stream = QTextStream(style_file)
        app.setStyleSheet(stream.readAll())
    else:
        print(f"Error al cargar styles.qss. Ruta: {os.path.join(BASE_DIR, 'Recursos/styles.qss')}")


    # Iniciar la ventana principal
    ventana_principal = VentanaPrincipal()
    ventana_principal.show()

    sys.exit(app.exec_())
