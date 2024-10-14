# ventanas/registro.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from db import obtener_conexion

class VentanaRegistro(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registro de Usuario")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        # Campo para Nombre
        self.nombre_label = QLabel("Nombre:")
        self.nombre_input = QLineEdit()
        layout.addWidget(self.nombre_label)
        layout.addWidget(self.nombre_input)

        # Campo para Clave
        self.clave_label = QLabel("Clave:")
        self.clave_input = QLineEdit()
        self.clave_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.clave_label)
        layout.addWidget(self.clave_input)

        # Campo para Seleccionar Rol
        self.rol_label = QLabel("Rol:")
        self.rol_input = QComboBox()
        self.rol_input.addItems(["Caja"])  # Solo se puede registrar como "Caja"
        layout.addWidget(self.rol_label)
        layout.addWidget(self.rol_input)

        # Botón para registrar
        self.btn_registrar = QPushButton("Registrar")
        self.btn_registrar.clicked.connect(self.registrar_usuario)
        layout.addWidget(self.btn_registrar)

        self.setLayout(layout)

    def registrar_usuario(self):
        nombre = self.nombre_input.text()
        clave = self.clave_input.text()
        rol = self.rol_input.currentText()

        if not nombre or not clave:
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")
            return

        # Guardar en la base de datos
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuario (nombre, clave, rol) VALUES (%s, %s, %s)", (nombre, clave, rol))
        conn.commit()
        cursor.close()
        conn.close()

        QMessageBox.information(self, "Registro Exitoso", "El usuario ha sido registrado.")
        self.close()
