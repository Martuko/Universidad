# ventanas/inicio_sesion.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox
from .caja import VentanaCaja
from .administrador import VentanaAdministrador
from .seleccion_rol import VentanaSeleccionRol
from db import obtener_conexion  # Asegúrate de importar tu función de conexión

class VentanaInicio(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inicio de Sesión")
        self.setGeometry(100, 100, 300, 300)

        # Layout principal
        layout = QVBoxLayout()

        # Usar un formulario para la disposición
        form_layout = QFormLayout()

        # Campo de Usuario
        self.usuario_label = QLabel("Usuario:")
        self.usuario_input = QLineEdit()
        form_layout.addRow(self.usuario_label, self.usuario_input)

        # Campo de Clave
        self.clave_label = QLabel("Clave:")
        self.clave_input = QLineEdit()
        self.clave_input.setEchoMode(QLineEdit.Password)
        form_layout.addRow(self.clave_label, self.clave_input)

        # Botón para iniciar sesión
        self.btn_iniciar = QPushButton("Iniciar Sesión")
        self.btn_iniciar.clicked.connect(self.iniciar_sesion)
        form_layout.addRow(self.btn_iniciar)

        # Botón para Registro
        self.btn_registro = QPushButton("Registrarse")
        self.btn_registro.clicked.connect(self.mostrar_registro)
        form_layout.addRow(self.btn_registro)

        layout.addLayout(form_layout)
        self.setLayout(layout)

    def iniciar_sesion(self):
        usuario = self.usuario_input.text()
        clave = self.clave_input.text()
        
        # Conexión a la base de datos
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuario WHERE username = %s AND password = %s", (usuario, clave))
            result = cursor.fetchone()
            cursor.close()
            conn.close()

            if result:
                # Abrir ventana de selección de rol
                self.ventana_seleccion_rol = VentanaSeleccionRol(result)
                self.ventana_seleccion_rol.show()
                self.close()
            else:
                QMessageBox.warning(self, "Error", "Usuario o clave incorrecta.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo conectar a la base de datos: {str(e)}")


    def seleccion_rol(self):
        # Crear una ventana emergente para seleccionar el rol (Caja o Administrador)
        rol_dialog = QWidget()
        rol_dialog.setWindowTitle("Seleccionar Rol")
        rol_dialog.setGeometry(100, 100, 300, 150)

        layout = QVBoxLayout()
        
        # Botones para seleccionar rol
        btn_admin = QPushButton("Ir a Administrador")
        btn_admin.clicked.connect(self.ir_administrador)
        layout.addWidget(btn_admin)

        btn_caja = QPushButton("Ir a Caja")
        btn_caja.clicked.connect(self.ir_caja)
        layout.addWidget(btn_caja)

        rol_dialog.setLayout(layout)
        rol_dialog.show()

    def ir_administrador(self):
        self.admin_ventana = VentanaAdministrador()
        self.admin_ventana.show()

    def ir_caja(self):
        self.caja_ventana = VentanaCaja()
        self.caja_ventana.show()

    def mostrar_registro(self):
        # Implementar lógica para mostrar ventana de registro
        from .registro import VentanaRegistro  # Importa la ventana de registro
        self.registro_ventana = VentanaRegistro()
        self.registro_ventana.show()
