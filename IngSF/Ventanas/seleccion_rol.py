from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox, QHBoxLayout , QFrame
)
from PyQt5.QtCore import Qt
import os
from PyQt5.QtGui import QPixmap
from .caja import VentanaCaja
from .administrador import VentanaAdministrador
from db import obtener_conexion


class VentanaSeleccionRol(QWidget):
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.setWindowTitle("Seleccionar Rol")
        self.setGeometry(100, 100, 900, 700)  # Tamaño de la ventana ajustado
        self.sucursal_id = None

        # Layout principal
        layout_principal = QVBoxLayout()
        layout_principal.setContentsMargins(0, 30, 0, 0)  # Reducir el margen superior para subir todo (30 píxeles)
        layout_principal.setSpacing(10)  # Espaciado entre layouts internos
        layout_principal.setAlignment(Qt.AlignTop)
        # Barra superior con el logo
        barra_superior = QHBoxLayout()
        barra_superior.setContentsMargins(20, 5, 20, 0)  # Ajustar márgenes para acercar el logo al borde superior
        barra_superior.setSpacing(5)  # Espaciado entre los elementos en la barra superior

        # Agregar barra superior al layout principal
        layout_principal.addLayout(barra_superior)

        # Layout central para los widgets
        layout_central = QVBoxLayout()
        layout_central.setAlignment(Qt.AlignTop)  # Alinear elementos al tope
        layout_central.setSpacing(20)  # Espaciado entre widgets
        layout_principal.addLayout(layout_central)

        self.setLayout(layout_principal)  # Establecer layout principal
        # Logo
        base_dir = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(base_dir, "../Recursos/logo.png")
        logo_label = QLabel()
        if os.path.exists(logo_path):  # Verifica si el archivo existe
            logo_pixmap = QPixmap(logo_path).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(logo_pixmap)
        else:
            logo_label.setText("Logo no encontrado")

        # Estilo transparente para el QLabel del logo
        logo_label.setStyleSheet("background-color: transparent; border: none;")
        barra_superior.addWidget(logo_label)

        # Espaciador para empujar el logo hacia la esquina superior izquierda
        barra_superior.addStretch()

        # Contenedor central para los elementos
        layout_central = QVBoxLayout()
        layout_central.setAlignment(Qt.AlignCenter)
        layout_central.setSpacing(20)  # Espaciado entre elementos

        # Etiqueta de bienvenida (sin caja)
        bienvenida_label = QLabel(f"Bienvenido, {self.usuario[1]}")
        bienvenida_label.setAlignment(Qt.AlignCenter)
        bienvenida_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #6b4226;  /* Café oscuro */
            background-color: transparent;
        """)
        layout_central.addWidget(bienvenida_label)

        # ComboBox para seleccionar sucursal (sin "contenedor")
        sucursal_label = QLabel("Selecciona una Sucursal:")
        sucursal_label.setAlignment(Qt.AlignCenter)
        sucursal_label.setStyleSheet("""
            font-size: 18px;
            color: #6b4226; /* Café oscuro */
            background-color: transparent;
        """)
        layout_central.addWidget(sucursal_label)

        self.sucursal_combo = QComboBox()
        self.sucursal_combo.setObjectName("sucursalCombo")
        self.sucursal_combo.setStyleSheet("""
            QComboBox {
                font-size: 16px;
                padding: 8px;
                border-radius: 10px;
                border: 1px solid #b38b6d; /* Café suave */
                background-color: #fff5ee; /* Fondo blanco */
            }
            QComboBox::drop-down {
                border: none;
            }
        """)
        layout_central.addWidget(self.sucursal_combo)

        # Cargar sucursales asociadas al usuario
        self.cargar_sucursales()

        # Botón para seleccionar Caja
        self.btn_caja = QPushButton("Ingresar como Caja")
        self.btn_caja.setObjectName("btnCaja")
        self.btn_caja.setStyleSheet("""
            QPushButton {
                font-size: 18px;
                color: white;
                background-color: #b38b6d; /* Café suave */
                border-radius: 12px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #6b4226; /* Café oscuro */
            }
        """)
        self.btn_caja.clicked.connect(self.abrir_ventana_caja)
        layout_central.addWidget(self.btn_caja)

        # Botón para seleccionar Administrador
        self.btn_administrador = QPushButton("Ingresar como Administrador")
        self.btn_administrador.setObjectName("btnAdmin")
        self.btn_administrador.setStyleSheet("""
            QPushButton {
                font-size: 18px;
                color: white;
                background-color: #b38b6d; /* Café suave */
                border-radius: 12px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #6b4226; /* Café oscuro */
            }
        """)
        self.btn_administrador.clicked.connect(self.mostrar_campo_clave_admin)
        layout_central.addWidget(self.btn_administrador)

        # Agregar layouts al principal
        layout_principal.addLayout(barra_superior)
        layout_principal.addLayout(layout_central)
        self.setLayout(layout_principal)

    def cargar_sucursales(self):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT s.idSucursal, s.nombre FROM us_su us JOIN sucursal s ON us.idSucursal = s.idSucursal WHERE us.idUsuario = %s",
                (self.usuario[0],)
            )
            sucursales = cursor.fetchall()
            self.sucursal_combo.clear()
            for sucursal in sucursales:
                self.sucursal_combo.addItem(sucursal[1], sucursal[0])
            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo conectar a la base de datos: {str(e)}")

    def abrir_ventana_caja(self):
        self.sucursal_id = self.sucursal_combo.currentData()
        if self.sucursal_id is not None:
            try:
                self.ventana_caja = VentanaCaja(self.usuario, self.sucursal_id,ventana_anterior=self)
                self.ventana_caja.show()
                self.close()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Ocurrió un error al abrir la ventana de Caja: {str(e)}")
        else:
            QMessageBox.warning(self, "Error", "Por favor, seleccione una sucursal antes de continuar.")

    def mostrar_campo_clave_admin(self):
        self.clave_label.show()
        self.clave_input.show()
        self.btn_confirmar_admin.show()

    def verificar_clave_admin(self):
        clave_ingresada = self.clave_input.text()
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute("SELECT password FROM usuario WHERE username = %s", (self.usuario[1],))
            clave_real = cursor.fetchone()
            cursor.close()
            conn.close()

            if clave_real and clave_real[0] == clave_ingresada:
                self.sucursal_id = self.sucursal_combo.currentData()
                self.ventana_admin = VentanaAdministrador(self.usuario, self.sucursal_id)
                self.ventana_admin.show()
                self.close()
            else:
                QMessageBox.warning(self, "Error", "Clave incorrecta.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo conectar a la base de datos: {str(e)}")
