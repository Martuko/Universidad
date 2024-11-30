# main.py
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QStackedWidget, QLabel, QHBoxLayout
from Ventanas.inicio_sesion import VentanaInicio
from Ventanas.caja import VentanaCaja
from Ventanas.administrador import VentanaAdministrador

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
        self.menu_lateral = QVBoxLayout()
        self.btn_inicio = QPushButton("Inicio de Sesión")
        self.btn_caja = QPushButton("Caja")
        self.btn_administrador = QPushButton("Administrador")
        
        # Conectar botones del menú
        self.btn_inicio.clicked.connect(lambda: self.cambiar_vista(0))
        self.btn_caja.clicked.connect(lambda: self.cambiar_vista(1))
        self.btn_administrador.clicked.connect(lambda: self.cambiar_vista(2))

       

        main_layout.addLayout(self.menu_lateral)

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
    ventana_principal = VentanaPrincipal()
    ventana_principal.show()
    sys.exit(app.exec_())