# ventanas/administrador.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QMessageBox, QDialog, QFormLayout, QLineEdit, QComboBox, QCheckBox
from db import obtener_conexion

class VentanaAdministrador(QWidget):
    def __init__(self, usuario, sucursal_id):
        super().__init__()
        self.usuario = usuario  # Almacenar información del usuario
        self.sucursal_id = sucursal_id  # ID de la sucursal seleccionada
        self.setWindowTitle("Administrador - Gestión de Inventario")
        self.setGeometry(100, 100, 600, 500)

        layout = QVBoxLayout()

        # Etiqueta de sucursal seleccionada
        self.sucursal_label = QLabel(f"Sucursal seleccionada: {self.obtener_nombre_sucursal()}")
        layout.addWidget(self.sucursal_label)

        # Botón para ver inventario
        self.btn_ver_inventario = QPushButton("Ver Inventario")
        self.btn_ver_inventario.clicked.connect(self.ver_inventario)
        layout.addWidget(self.btn_ver_inventario)

        # Botón para agregar producto
        self.btn_agregar_producto = QPushButton("Agregar Producto")
        self.btn_agregar_producto.clicked.connect(self.agregar_producto)
        layout.addWidget(self.btn_agregar_producto)

        # Botón para eliminar producto
        self.btn_eliminar_producto = QPushButton("Eliminar Producto")
        self.btn_eliminar_producto.clicked.connect(self.eliminar_producto)
        layout.addWidget(self.btn_eliminar_producto)

        # Botón para ver estadísticas
        self.btn_ver_estadisticas = QPushButton("Ver Estadísticas")
        layout.addWidget(self.btn_ver_estadisticas)

        self.setLayout(layout)

    def obtener_nombre_sucursal(self):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute("SELECT nombre_sucursal FROM sucursal WHERE id_sucursal = %s", (self.sucursal_id,))
            sucursal = cursor.fetchone()
            cursor.close()
            conn.close()
            return sucursal[0] if sucursal else "Sucursal no encontrada"
        except Exception as e:
            return f"Error al obtener nombre: {str(e)}"

    def ver_inventario(self):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT p.Codigo_Producto, p.Nombre_Producto, p.Valor_Producto, i.Cantidad, cp.Nombre_Categoria
                FROM Producto p
                JOIN Inventario i ON p.ID_Producto = i.ID_Producto
                LEFT JOIN Categoria_Producto cp ON p.ID_Categoria = cp.ID_Categoria
                WHERE i.ID_Sucursal = %s
            """, (self.sucursal_id,))
            productos = cursor.fetchall()

            if not productos:
                QMessageBox.information(self, "Inventario vacío", "No hay productos en el inventario para esta sucursal.")
                return

            inventario_window = QDialog(self)
            inventario_window.setWindowTitle("Inventario de Sucursal")
            inventario_layout = QVBoxLayout()

            inventario_table = QTableWidget()
            inventario_table.setColumnCount(5)
            inventario_table.setHorizontalHeaderLabels(["Código Producto", "Nombre del Producto", "Valor", "Cantidad", "Categoría"])

            for row_index, (codigo, nombre, valor, cantidad, categoria) in enumerate(productos):
                inventario_table.insertRow(row_index)
                inventario_table.setItem(row_index, 0, QTableWidgetItem(codigo))
                inventario_table.setItem(row_index, 1, QTableWidgetItem(nombre))
                inventario_table.setItem(row_index, 2, QTableWidgetItem(f"${valor}"))
                inventario_table.setItem(row_index, 3, QTableWidgetItem(str(cantidad)))
                inventario_table.setItem(row_index, 4, QTableWidgetItem(categoria or "Sin categoría"))

            inventario_layout.addWidget(inventario_table)
            inventario_window.setLayout(inventario_layout)
            inventario_window.setGeometry(100, 100, 700, 400)
            inventario_window.exec_()

            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo conectar a la base de datos: {str(e)}")

    def agregar_producto(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Agregar Producto")
        form_layout = QFormLayout()

        self.tipo_producto = QComboBox()
        self.tipo_producto.addItem("Nuevo Producto")
        self.tipo_producto.addItem("Producto Existente")

        # Campos de entrada
        self.codigo_producto_input = QLineEdit()
        self.nombre_producto_input = QLineEdit()  # Solo para nuevos productos
        self.valor_producto_input = QLineEdit()   # Solo para nuevos productos
        self.cantidad_producto_input = QLineEdit()

        # Combobox para seleccionar la categoría
        self.categoria_combo = QComboBox()
        self.cargar_categorias()

        form_layout.addRow("Tipo de Producto:", self.tipo_producto)
        form_layout.addRow("Código del Producto:", self.codigo_producto_input)
        form_layout.addRow("Nombre del Producto:", self.nombre_producto_input)
        form_layout.addRow("Valor del Producto:", self.valor_producto_input)
        form_layout.addRow("Cantidad del Producto:", self.cantidad_producto_input)
        form_layout.addRow("Categoría:", self.categoria_combo)

        self.tipo_producto.currentIndexChanged.connect(self.toggle_producto_fields)
        btn_guardar = QPushButton("Guardar")
        btn_guardar.clicked.connect(lambda: self.guardar_producto(dialog))
        form_layout.addRow(btn_guardar)

        dialog.setLayout(form_layout)
        dialog.exec_()
        self.toggle_producto_fields()

    def cargar_categorias(self):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute("SELECT id_categoria, nombre_categoria FROM Categoria_Producto")
            categorias = cursor.fetchall()
            for categoria in categorias:
                self.categoria_combo.addItem(categoria[1], categoria[0])
            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar las categorías: {str(e)}")

    def toggle_producto_fields(self):
        if self.tipo_producto.currentText() == "Nuevo Producto":
            self.nombre_producto_input.show()
            self.valor_producto_input.show()
            self.categoria_combo.show()
        else:
            self.nombre_producto_input.hide()
            self.valor_producto_input.hide()
            self.categoria_combo.hide()

    def guardar_producto(self, dialog):
        codigo = self.codigo_producto_input.text()
        nombre = self.nombre_producto_input.text()
        valor = self.valor_producto_input.text()
        cantidad = self.cantidad_producto_input.text()

        if not codigo or (self.tipo_producto.currentText() == "Nuevo Producto" and (not nombre or not valor)) or not cantidad:
            QMessageBox.warning(self, "Error", "Por favor complete todos los campos")
            return
        
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()

            if self.tipo_producto.currentText() == "Nuevo Producto":
                cursor.execute(
                    "INSERT INTO Producto (Codigo_Producto, Nombre_Producto, Valor_Producto, ID_Categoria) VALUES (%s, %s, %s, %s)",
                    (codigo, nombre, valor, self.categoria_combo.currentData())
                )
                conn.commit()
                cursor.execute("SELECT ID_Producto FROM Producto WHERE Codigo_Producto = %s", (codigo,))
                id_producto = cursor.fetchone()[0]
                cursor.execute(
                    "INSERT INTO Inventario (ID_Sucursal, ID_Producto, Cantidad) VALUES (%s, %s, %s)",
                    (self.sucursal_id, id_producto, cantidad)
                )
                QMessageBox.information(self, "Éxito", "Producto agregado exitosamente")
                
            elif self.tipo_producto.currentText() == "Producto Existente":
                cursor.execute("SELECT ID_Producto FROM Producto WHERE Codigo_Producto = %s", (codigo,))
                producto = cursor.fetchone()
                if producto:
                    id_producto = producto[0]
                    cursor.execute(
                        "UPDATE Inventario SET Cantidad = Cantidad + %s WHERE ID_Producto = %s AND ID_Sucursal = %s",
                        (cantidad, id_producto, self.sucursal_id)
                    )
                    QMessageBox.information(self, "Éxito", "Cantidad actualizada exitosamente")
                else:
                    QMessageBox.warning(self, "Error", "Producto no encontrado.")
            
            conn.commit()
            cursor.close()
            conn.close()
            dialog.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def eliminar_producto(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Eliminar Producto")
        form_layout = QFormLayout()

        codigo_producto_input = QLineEdit()
        cantidad_producto_input = QLineEdit()
        self.eliminar_todo_checkbox = QCheckBox("Eliminar todo el producto")

        form_layout.addRow("Código del Producto:", codigo_producto_input)
        form_layout.addRow("Cantidad a eliminar:", cantidad_producto_input)
        form_layout.addRow(self.eliminar_todo_checkbox)

        btn_eliminar = QPushButton("Eliminar")
        btn_eliminar.clicked.connect(lambda: self.confirmar_eliminar_producto(codigo_producto_input.text(), cantidad_producto_input.text(), dialog))
        form_layout.addRow(btn_eliminar)

        dialog.setLayout(form_layout)
        dialog.exec_()

    def confirmar_eliminar_producto(self, codigo, cantidad, dialog):
        if not codigo or (not cantidad and not self.eliminar_todo_checkbox.isChecked()):
            QMessageBox.warning(self, "Error", "Por favor ingrese el código del producto y la cantidad o seleccione 'Eliminar todo el producto'")
            return

        try:
            conn = obtener_conexion()
            cursor = conn.cursor()

            if self.eliminar_todo_checkbox.isChecked():
                cursor.execute(
                    "DELETE FROM Inventario WHERE ID_Producto IN (SELECT ID_Producto FROM Producto WHERE Codigo_Producto = %s) AND ID_Sucursal = %s",
                    (codigo, self.sucursal_id)
                )
                cursor.execute(
                    "DELETE FROM Producto WHERE Codigo_Producto = %s",
                    (codigo,)
                )
                conn.commit()
                QMessageBox.information(self, "Éxito", "Producto eliminado exitosamente")
            else:
                cursor.execute(
                    "UPDATE Inventario SET Cantidad = Cantidad - %s WHERE ID_Producto IN (SELECT ID_Producto FROM Producto WHERE Codigo_Producto = %s) AND ID_Sucursal = %s",
                    (cantidad, codigo, self.sucursal_id)
                )
                conn.commit()
                QMessageBox.information(self, "Éxito", "Cantidad eliminada exitosamente")

            cursor.close()
            conn.close()
            dialog.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def ver_estadisticas(self):
        QMessageBox.information(self, "Información", "Función para ver estadísticas aún no implementada.")
