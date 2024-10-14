# ventanas/inicio_sesion.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from .caja import VentanaCaja
from .administrador import VentanaAdministrador

class VentanaInicio(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Inicio de Sesión")
        self.setGeometry(100, 100, 300, 200)
        
        # Layout principal
        layout = QVBoxLayout()
        
        # Usar un formulario para la disposición
        form_layout = QFormLayout()
        
        # Botón para Caja
        self.btn_caja = QPushButton("Iniciar como Caja")
        self.btn_caja.clicked.connect(self.iniciar_caja)
        form_layout.addRow(self.btn_caja)

        # Botón para Administrador
        self.btn_admin = QPushButton("Iniciar como Administrador")
        self.btn_admin.clicked.connect(self.mostrar_campos_admin)
        form_layout.addRow(self.btn_admin)

        # Campo de Clave para Administrador
        self.clave_label = QLabel("Clave:")
        self.clave_input = QLineEdit()
        self.clave_input.setEchoMode(QLineEdit.Password)
        self.clave_input.hide()
        form_layout.addRow(self.clave_label, self.clave_input)

        # Campo de Usuario para Administrador
        self.usuario_label = QLabel("Usuario:")
        self.usuario_input = QLineEdit()
        self.usuario_input.hide()
        form_layout.addRow(self.usuario_label, self.usuario_input)

        # Botón para confirmar los datos del Administrador
        self.btn_confirmar_admin = QPushButton("Confirmar")
        self.btn_confirmar_admin.clicked.connect(self.iniciar_admin)
        self.btn_confirmar_admin.hide()
        form_layout.addRow(self.btn_confirmar_admin)

        layout.addLayout(form_layout)
        self.setLayout(layout)

    def mostrar_campos_admin(self):
        # Mostrar campos de usuario y clave y botón de confirmación
        self.usuario_label.show()
        self.usuario_input.show()
        self.clave_label.show()
        self.clave_input.show()
        self.btn_confirmar_admin.show()

    def iniciar_caja(self):
        # Lógica para iniciar la ventana de Caja
        self.close()
        self.caja_ventana = VentanaCaja()
        self.caja_ventana.show()

    def iniciar_admin(self):
        # Comprobación de las credenciales del Administrador
        usuario = self.usuario_input.text()
        clave = self.clave_input.text()
        
        # Cambia estos valores según lo que prefieras
        usuario_admin = "admin"
        clave_admin = "admin123"
        
        if usuario == usuario_admin and clave == clave_admin:
            self.close()
            self.admin_ventana = VentanaAdministrador()
            self.admin_ventana.show()
        else:
            QMessageBox.warning(self, "Error", "Usuario o clave incorrecta")
