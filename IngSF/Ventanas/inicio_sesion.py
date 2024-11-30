from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QFormLayout, QDialog
)
import os

from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtCore import Qt
from db import obtener_conexion  # Asegúrate de que esta función esté correctamente implementada
from Ventanas.seleccion_rol import VentanaSeleccionRol

class VentanaInicio(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inicio de Sesión")
        self.setGeometry(100, 100, 800, 600)

        
        # Layout principal
        layout_principal = QVBoxLayout(self)

        # Barra superior (botones y logo)
        barra_superior = QHBoxLayout()

        base_dir = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(base_dir, "../Recursos/logo.png")

        # Logo
        logo_label = QLabel()
        if os.path.exists(logo_path):  # Verifica si el archivo existe
            logo_pixmap = QPixmap(logo_path).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            if not logo_pixmap.isNull():  # Verifica si el logo se cargó correctamente
                logo_label.setPixmap(logo_pixmap)
                 # Centra el logo en el QLabel
            else:
                logo_label.setText("Error al cargar el logo")
        else:
            logo_label.setText("Archivo logo no encontrado")

        # Establece el fondo del QLabel como transparente
        logo_label.setStyleSheet("background-color: transparent; border: none;")

        # Agrega el logo al layout
        barra_superior.addWidget(logo_label)


        # Botones
        self.btn_iniciar = QPushButton("Iniciar Sesión")
        self.btn_iniciar.clicked.connect(self.mostrar_formulario_inicio)
        self.btn_registrar = QPushButton("Registrar")
        self.btn_registrar.clicked.connect(self.mostrar_formulario_registro)

        barra_superior.addWidget(self.btn_iniciar)
        barra_superior.addWidget(self.btn_registrar)

        layout_principal.addLayout(barra_superior)

        # Mensaje de bienvenida
        mensaje_bienvenida = QLabel("¡Bienvenido al sistema del Casino!")
        mensaje_bienvenida.setAlignment(Qt.AlignCenter)
        mensaje_bienvenida.setStyleSheet("font-size: 36px; font-weight: bold; margin-top: 20px;")
        layout_principal.addWidget(mensaje_bienvenida)

        # Contenedor para los formularios
        self.formulario_contenedor = QVBoxLayout()
        layout_principal.addLayout(self.formulario_contenedor)

        # Variable para almacenar sucursales asociadas
        self.sucursales_asociadas = []

    def mostrar_formulario_inicio(self):
        self.limpiar_formulario()
        formulario = QVBoxLayout()

        usuario_label = QLabel("Usuario:")
        self.usuario_input = QLineEdit()
        self.usuario_input.setPlaceholderText("Ingrese su usuario")
        formulario.addWidget(usuario_label)
        formulario.addWidget(self.usuario_input)

        clave_label = QLabel("Clave:")
        self.clave_input = QLineEdit()
        self.clave_input.setEchoMode(QLineEdit.Password)
        self.clave_input.setPlaceholderText("Ingrese su clave")
        formulario.addWidget(clave_label)
        formulario.addWidget(self.clave_input)

        btn_entrar = QPushButton("Entrar")
        btn_entrar.clicked.connect(self.iniciar_sesion)
        formulario.addWidget(btn_entrar)

        self.formulario_contenedor.addLayout(formulario)

    def mostrar_formulario_registro(self):
        self.limpiar_formulario()
        formulario = QVBoxLayout()

        nombre_label = QLabel("Nombre:")
        self.nombre_input = QLineEdit()
        self.nombre_input.setPlaceholderText("Ingrese su nombre")
        formulario.addWidget(nombre_label)
        formulario.addWidget(self.nombre_input)

        clave_label = QLabel("Clave:")
        self.clave_input = QLineEdit()
        self.clave_input.setEchoMode(QLineEdit.Password)
        self.clave_input.setPlaceholderText("Ingrese su clave")
        formulario.addWidget(clave_label)
        formulario.addWidget(self.clave_input)

        sucursales_label = QLabel("Cantidad de Sucursales:")
        self.sucursal_input = QLineEdit()
        self.sucursal_input.setPlaceholderText("Ingrese la cantidad de sucursales")
        formulario.addWidget(sucursales_label)
        formulario.addWidget(self.sucursal_input)

        btn_agregar_sucursales = QPushButton("Agregar Sucursales")
        btn_agregar_sucursales.clicked.connect(self.agregar_sucursales)
        formulario.addWidget(btn_agregar_sucursales)

        btn_registrar = QPushButton("Registrar")
        btn_registrar.clicked.connect(self.registrar_usuario)
        formulario.addWidget(btn_registrar)

        self.formulario_contenedor.addLayout(formulario)

    def limpiar_formulario(self):
        """Limpia todos los widgets existentes en el contenedor de formularios"""
        while self.formulario_contenedor.count():
            item = self.formulario_contenedor.takeAt(0)
            if item:
                if item.widget():
                    item.widget().deleteLater()
                elif item.layout():
                    self.limpiar_layout(item.layout())

    def limpiar_layout(self, layout):
        """Limpia los layouts anidados para evitar superposición de formularios"""
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.limpiar_layout(item.layout())

    def agregar_sucursales(self):
        cantidad = int(self.sucursal_input.text())
        for _ in range(cantidad):
            dialog = QDialog(self)
            dialog.setWindowTitle("Agregar Sucursal")
            form_layout = QFormLayout()

            nombre_sucursal_input = QLineEdit()
            direccion_sucursal_input = QLineEdit()

            form_layout.addRow("Nombre de Sucursal:", nombre_sucursal_input)
            form_layout.addRow("Dirección de Sucursal:", direccion_sucursal_input)

            btn_guardar = QPushButton("Guardar")
            btn_guardar.clicked.connect(lambda: self.guardar_sucursal(nombre_sucursal_input.text(), direccion_sucursal_input.text(), dialog))
            form_layout.addRow(btn_guardar)

            dialog.setLayout(form_layout)
            dialog.exec_()

    def guardar_sucursal(self, nombre, direccion, dialog):
        if not nombre or not direccion:
            QMessageBox.warning(self, "Error", "Por favor complete todos los campos.")
            return

        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            query = "INSERT INTO sucursal (nombre, ubicacion) VALUES (%s, %s) RETURNING idSucursal"
            cursor.execute(query, (nombre, direccion))
            id_sucursal = cursor.fetchone()[0]
            self.sucursales_asociadas.append(id_sucursal)
            conn.commit()
            cursor.close()
            conn.close()
            QMessageBox.information(self, "Éxito", f"Sucursal '{nombre}' agregada exitosamente.")
            dialog.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo registrar la sucursal: {str(e)}")

    def iniciar_sesion(self):
        usuario = self.usuario_input.text()
        clave = self.clave_input.text()

        if not usuario or not clave:
            QMessageBox.warning(self, "Error", "Por favor complete todos los campos.")
            return

        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            query = "SELECT * FROM usuario WHERE username = %s AND password = %s"
            cursor.execute(query, (usuario, clave))
            resultado = cursor.fetchone()
            cursor.close()
            conn.close()

            if resultado:
                QMessageBox.information(self, "Éxito", f"Bienvenido, {usuario}!")
                self.ventana_seleccion_rol = VentanaSeleccionRol(resultado)
                self.ventana_seleccion_rol.show()
                self.close()
            else:
                QMessageBox.warning(self, "Error", "Usuario o clave incorrecta.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo conectar a la base de datos: {str(e)}")

    def registrar_usuario(self):
        nombre = self.nombre_input.text()
        clave = self.clave_input.text()

        if not nombre or not clave:
            QMessageBox.warning(self, "Error", "Por favor complete todos los campos.")
            return

        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            query = "INSERT INTO usuario (username, password, type) VALUES (%s, %s, %s) RETURNING idUsuario"
            cursor.execute(query, (nombre, clave, "Administrador"))
            id_usuario = cursor.fetchone()[0]

            for id_sucursal in self.sucursales_asociadas:
                query = "INSERT INTO us_su (idUsuario, idSucursal) VALUES (%s, %s)"
                cursor.execute(query, (id_usuario, id_sucursal))

            conn.commit()
            cursor.close()
            conn.close()

            QMessageBox.information(self, "Éxito", "Usuario registrado correctamente.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo registrar el usuario: {str(e)}")
