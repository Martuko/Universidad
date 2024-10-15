# ventanas/registro.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QDialog, QFormLayout
import psycopg2
from psycopg2 import sql

class VentanaRegistro(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Registro de Usuario")
        self.setGeometry(100, 100, 300, 300)
        
        layout = QVBoxLayout()

        # Campo de Nombre
        self.nombre_label = QLabel("Nombre:")
        self.nombre_input = QLineEdit()
        layout.addWidget(self.nombre_label)
        layout.addWidget(self.nombre_input)

        # Campo de Clave
        self.clave_label = QLabel("Clave:")
        self.clave_input = QLineEdit()
        self.clave_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.clave_label)
        layout.addWidget(self.clave_input)

        # Campo de Sucursales
        self.sucursal_label = QLabel("Cantidad de Sucursales:")
        self.sucursal_input = QLineEdit()
        layout.addWidget(self.sucursal_label)
        layout.addWidget(self.sucursal_input)

        # Botón para agregar sucursales
        self.btn_agregar_sucursales = QPushButton("Agregar Sucursales")
        self.btn_agregar_sucursales.clicked.connect(self.agregar_sucursales)
        layout.addWidget(self.btn_agregar_sucursales)

        # Botón de Registro
        self.btn_registrar = QPushButton("Registrar")
        self.btn_registrar.clicked.connect(self.registrar_usuario)
        layout.addWidget(self.btn_registrar)

        self.setLayout(layout)

        # Almacenar las sucursales asociadas
        self.sucursales_asociadas = []

    def agregar_sucursales(self):
        # Lógica para agregar sucursales según la cantidad ingresada
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
        # Guardar sucursal en la base de datos
        if not nombre or not direccion:
            QMessageBox.warning(self, "Error", "Por favor complete todos los campos")
            return
        
        try:
            conn = psycopg2.connect("postgres://u704a5ln8sar5c:pb91fd1049f61702a300d7ed31f7984963e5837e9788c2febf90465f105ef05a3@ce0lkuo944ch99.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d4ra8hg5s8stsv")
            cursor = conn.cursor()
            cursor.execute(
                sql.SQL("INSERT INTO sucursal (Nombre_Sucursal, Ubicacion) VALUES (%s, %s) RETURNING id_sucursal"),
                [nombre, direccion]
            )
            id_sucursal = cursor.fetchone()[0]  # Obtener el ID de la sucursal creada
            self.sucursales_asociadas.append(id_sucursal)  # Agregar a la lista de sucursales asociadas
            conn.commit()
            cursor.close()
            conn.close()
            QMessageBox.information(self, "Éxito", "Sucursal agregada exitosamente")
            dialog.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def registrar_usuario(self):
        nombre = self.nombre_input.text()
        clave = self.clave_input.text()
        rol = 'Administrador'  # Asignar el rol de Administrador por defecto

        # Validar entrada
        if not nombre or not clave:
            QMessageBox.warning(self, "Error", "Por favor complete todos los campos")
            return

        # Conexión a la base de datos
        try:
            conn = psycopg2.connect("postgres://u704a5ln8sar5c:pb91fd1049f61702a300d7ed31f7984963e5837e9788c2febf90465f105ef05a3@ce0lkuo944ch99.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d4ra8hg5s8stsv")
            cursor = conn.cursor()
            cursor.execute(
                sql.SQL("INSERT INTO usuario (nombre, clave, rol) VALUES (%s, %s, %s) RETURNING id_usuario"),
                [nombre, clave, rol]
            )
            id_usuario = cursor.fetchone()[0]  # Obtener el ID del usuario creado
            conn.commit()

            # Asociar el usuario a las sucursales
            for id_sucursal in self.sucursales_asociadas:
                cursor.execute(
                    sql.SQL("INSERT INTO usuario_sucursal (id_usuario, id_sucursal) VALUES (%s, %s)"),
                    [id_usuario, id_sucursal]
                )

            conn.commit()  # Confirmar las inserciones de la tabla intermedia
            cursor.close()
            conn.close()
            QMessageBox.information(self, "Éxito", "Usuario registrado exitosamente con sucursales asociadas")
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
