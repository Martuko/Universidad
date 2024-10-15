# ventanas/seleccion_rol.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from .caja import VentanaCaja
from .administrador import VentanaAdministrador
from db import obtener_conexion

class VentanaSeleccionRol(QWidget):
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.setWindowTitle("Seleccionar Rol")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        # Etiqueta de bienvenida con el nombre del usuario
        bienvenida_label = QLabel(f"Bienvenido, {self.usuario[1]}")
        layout.addWidget(bienvenida_label)

        # Botón para seleccionar Caja
        self.btn_caja = QPushButton("Ingresar como Caja")
        self.btn_caja.clicked.connect(self.abrir_ventana_caja)
        layout.addWidget(self.btn_caja)

        # Botón para seleccionar Administrador
        self.btn_administrador = QPushButton("Ingresar como Administrador")
        self.btn_administrador.clicked.connect(self.mostrar_campo_clave_admin)
        layout.addWidget(self.btn_administrador)

        # Campo de Clave de administrador, oculto por defecto
        self.clave_label = QLabel(f"Clave del usuario {self.usuario[1]}:")
        self.clave_input = QLineEdit()
        self.clave_input.setEchoMode(QLineEdit.Password)
        self.clave_label.hide()
        self.clave_input.hide()
        layout.addWidget(self.clave_label)
        layout.addWidget(self.clave_input)

        # Botón para confirmar la contraseña del administrador
        self.btn_confirmar_admin = QPushButton("Confirmar")
        self.btn_confirmar_admin.clicked.connect(self.verificar_clave_admin)
        self.btn_confirmar_admin.hide()
        layout.addWidget(self.btn_confirmar_admin)

        self.setLayout(layout)

    def mostrar_campo_clave_admin(self):
        # Mostrar campo de clave y botón de confirmar para el rol de Administrador
        self.clave_label.show()
        self.clave_input.show()
        self.btn_confirmar_admin.show()

    def abrir_ventana_caja(self):
        # Lógica para abrir la ventana de Caja
        self.ventana_caja = VentanaCaja()
        self.ventana_caja.show()
        self.close()

    def verificar_clave_admin(self):
        # Verificar la clave de administrador
        clave_ingresada = self.clave_input.text()
        
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute("SELECT clave FROM usuario WHERE nombre = %s", (self.usuario[1],))
            clave_real = cursor.fetchone()
            cursor.close()
            conn.close()

            if clave_real and clave_real[0] == clave_ingresada:
                self.ventana_admin = VentanaAdministrador()
                self.ventana_admin.show()
                self.close()
            else:
                QMessageBox.warning(self, "Error", "Clave incorrecta.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo conectar a la base de datos: {str(e)}")
