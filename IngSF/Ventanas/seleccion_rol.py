# ventanas/seleccion_rol.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox
from .caja import VentanaCaja
from .administrador import VentanaAdministrador
from db import obtener_conexion

class VentanaSeleccionRol(QWidget):
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.setWindowTitle("Seleccionar Rol")
        self.setGeometry(100, 100, 300, 300)

        layout = QVBoxLayout()

        # Etiqueta de bienvenida con el nombre del usuario
        bienvenida_label = QLabel(f"Bienvenido, {self.usuario[1]}")
        layout.addWidget(bienvenida_label)

        # ComboBox para seleccionar sucursal
        self.sucursal_combo = QComboBox()
        layout.addWidget(QLabel("Selecciona una Sucursal:"))
        layout.addWidget(self.sucursal_combo)

        # Cargar sucursales asociadas al usuario
        self.cargar_sucursales()

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

    def cargar_sucursales(self):
    # Cargar sucursales asociadas al usuario
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute(
            "SELECT s.id_sucursal, s.nombre_sucursal FROM usuario_sucursal us JOIN sucursal s ON us.id_sucursal = s.id_sucursal WHERE us.id_usuario = %s",
            (self.usuario[0],)  # Suponiendo que el ID de usuario está en el índice 0
            )
            sucursales = cursor.fetchall()

        # Limpiar el combo box antes de agregar nuevas sucursales
            self.sucursal_combo.clear()

            for sucursal in sucursales:
            # Agregar tanto el nombre como el ID de la sucursal
                self.sucursal_combo.addItem(sucursal[1], sucursal[0])  # agregar nombre y ID

            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo conectar a la base de datos: {str(e)}")

    def abrir_ventana_caja(self):
        # Lógica para abrir la ventana de Caja, pasando la sucursal seleccionada
        sucursal_seleccionada = self.sucursal_combo.currentData()  # Obtener el ID de la sucursal
        if sucursal_seleccionada is not None:  # Comprobar que se haya seleccionado una sucursal
            try:
                print(f"Sucursal seleccionada: {sucursal_seleccionada}")  # Debug
                self.ventana_caja = VentanaCaja(sucursal_id=sucursal_seleccionada)  # Asegúrate de pasar el ID de sucursal
                self.ventana_caja.show()
                self.close()  # Cerrar la ventana de selección de rol
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Ocurrió un error al abrir la ventana de Caja: {str(e)}")
        else:
            QMessageBox.warning(self, "Error", "Por favor, seleccione una sucursal antes de continuar.")


    def mostrar_campo_clave_admin(self):
        # Mostrar campo de clave y botón de confirmar para el rol de Administrador
        self.clave_label.show()
        self.clave_input.show()
        self.btn_confirmar_admin.show()

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
                # Obtener el ID de la sucursal seleccionada
                sucursal_id = self.sucursal_combo.currentData()  # Asegúrate de que la sucursal_combo tenga datos

                # Pasar el ID de la sucursal y el usuario a la ventana del administrador
                self.ventana_admin = VentanaAdministrador(self.usuario, sucursal_id) 
                self.ventana_admin.show()
                self.close()
            else:
                QMessageBox.warning(self, "Error", "Clave incorrecta.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo conectar a la base de datos: {str(e)}")
