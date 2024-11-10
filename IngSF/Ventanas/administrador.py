# ventanas/administrador.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QMessageBox, QDialog, QFormLayout, QLineEdit, QComboBox, QCheckBox
from db import obtener_conexion

class VentanaAdministrador(QWidget):
    def __init__(self, usuario, sucursal_id,ventana_anterior=None):
        super().__init__()
        self.usuario = usuario  # Almacenar información del usuario
        self.sucursal_id = sucursal_id  # ID de la sucursal seleccionada
        self.setWindowTitle("Administrador - Gestión de Inventario")
        self.setGeometry(100, 100, 600, 500)
        self.verificar_inventario_bajo()
        self.ventana_anterior = ventana_anterior

        layout = QVBoxLayout()

        self.sucursal_combo = QComboBox()
        self.cargar_sucursales()
        self.sucursal_combo.setCurrentText(self.obtener_nombre_sucursal())
        self.sucursal_combo.currentIndexChanged.connect(self.cambiar_sucursal)
        layout.addWidget(QLabel("Seleccionar Sucursal:"))
        layout.addWidget(self.sucursal_combo)

        self.btn_regresar = QPushButton("Regresar")
        self.btn_regresar.clicked.connect(self.regresar)
        layout.addWidget(self.btn_regresar)

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

        # Botón para ver inventario de la cocina
        self.btn_ver_inventario_cocina = QPushButton("Ver Inventario Cocina")
        self.btn_ver_inventario_cocina.clicked.connect(self.ver_inventario_cocina)
        layout.addWidget(self.btn_ver_inventario_cocina)

        # Botón para agregar productos al inventario de cocina
        self.btn_agregar_producto_cocina = QPushButton("Agregar Producto a Cocina")
        self.btn_agregar_producto_cocina.clicked.connect(self.agregar_producto_cocina)
        layout.addWidget(self.btn_agregar_producto_cocina)

        self.btn_eliminar_producto_cocina = QPushButton("Eliminar Producto de Inventario de Cocina")
        self.btn_eliminar_producto_cocina.clicked.connect(self.eliminar_producto_cocina)
        layout.addWidget(self.btn_eliminar_producto_cocina)
        
        self.btn_traspasar_producto_cocina = QPushButton("Traspasar Producto entre Sucursales")
        self.btn_traspasar_producto_cocina.clicked.connect(self.traspasar_producto_cocina)
        layout.addWidget(self.btn_traspasar_producto_cocina)
                # Botón para ver estadísticas
        self.btn_ver_estadisticas = QPushButton("Ver Estadísticas")
        layout.addWidget(self.btn_ver_estadisticas)



        if self.ventana_anterior:
            btn_regresar = QPushButton("Regresar")
            btn_regresar.clicked.connect(self.regresar)
            layout.addWidget(btn_regresar)

        self.setLayout(layout)


    def cargar_sucursales(self):
        # Cargar sucursales disponibles en el combo box
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT s.idSucursal, s.nombre 
                FROM sucursal s
                JOIN us_su us ON s.idSucursal = us.idSucursal
                WHERE us.idUsuario = %s
            """, (self.usuario[0],))
            sucursales = cursor.fetchall()

            self.sucursal_combo.clear()
            for sucursal in sucursales:
                self.sucursal_combo.addItem(sucursal[1], sucursal[0])

            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar las sucursales: {str(e)}")

    def obtener_nombre_sucursal(self):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute("SELECT nombre FROM sucursal WHERE idSucursal = %s", (self.sucursal_id,))
            sucursal = cursor.fetchone()
            cursor.close()
            conn.close()
            return sucursal[0] if sucursal else "Sucursal no encontrada"
        except Exception as e:
            return f"Error al obtener nombre: {str(e)}"

    def cambiar_sucursal(self):
        # Cambiar la sucursal seleccionada
        self.sucursal_id = self.sucursal_combo.currentData()
        # Llamar a funciones para actualizar la interfaz de acuerdo con la nueva sucursal
        self.actualizar_datos_sucursal()

    def actualizar_datos_sucursal(self):
        # Aquí debes actualizar los datos mostrados en la ventana de acuerdo a la sucursal seleccionada
        self.sucursal_label.setText(f"Sucursal seleccionada: {self.obtener_nombre_sucursal()}")
        self.verificar_inventario_bajo()  # Puedes llamar a esta función para verificar el inventario bajo en la nueva sucursal


    def regresar(self):
        self.close()
        if self.ventana_anterior:
            self.ventana_anterior.show()

    def obtener_nombre_sucursal(self):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute("SELECT nombre FROM sucursal WHERE idSucursal = %s", (self.sucursal_id,))
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
                SELECT p.codProducto, p.nProducto, p.valor, i.cantStock, c.nCategoria
                FROM productos p
                JOIN inventario i ON p.idProducto = i.idProducto
                LEFT JOIN categorias c ON p.idCategoria = c.idCategoria
                WHERE i.idSucursal = %s
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
            cursor.execute("SELECT idCategoria, nCategoria FROM Categorias")
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
                    "INSERT INTO productos (codProducto, nProducto, valor, idCategoria) VALUES (%s, %s, %s, %s)",
                    (codigo, nombre, valor, self.categoria_combo.currentData())
                )

                conn.commit()
                cursor.execute("SELECT idProducto FROM productos WHERE codProducto = %s", (codigo,))             
                id_producto = cursor.fetchone()[0]
                cursor.execute(
                    "INSERT INTO inventario (idSucursal, idProducto, cantStock) VALUES (%s, %s, %s)",
                    (self.sucursal_id, id_producto, cantidad)
                )

                QMessageBox.information(self, "Éxito", "Producto agregado exitosamente")
                
            elif self.tipo_producto.currentText() == "Producto Existente":
                cursor.execute("SELECT idProducto FROM productos WHERE codProducto = %s", (codigo,))      
                producto = cursor.fetchone()
                if producto:
                    id_producto = producto[0]
                    cursor.execute(
                        "UPDATE inventario SET cantStock = cantStock + %s WHERE idProducto = %s AND idSucursal = %s",
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
                # Eliminar completamente el producto tanto de 'inventario' como de 'productos'
                cursor.execute("""
                    DELETE FROM inventario WHERE idProducto IN (SELECT idProducto FROM productos WHERE codProducto = %s) AND idSucursal = %s
                """, (codigo, self.sucursal_id))
                cursor.execute("DELETE FROM productos WHERE codProducto = %s", (codigo,))

                conn.commit()
                QMessageBox.information(self, "Éxito", "Producto eliminado completamente de la base de datos.")
            else:
                # Verificar el stock actual
                cursor.execute("""
                    SELECT cantStock FROM inventario
                    WHERE idProducto IN (SELECT idProducto FROM productos WHERE codProducto = %s) AND idSucursal = %s
                """, (codigo, self.sucursal_id))
                resultado = cursor.fetchone()

                if not resultado:
                    QMessageBox.warning(self, "Error", "El producto no existe en el inventario de esta sucursal.")
                    return

                stock_actual = resultado[0]

                # Verificar que haya suficiente stock para eliminar
                if stock_actual < int(cantidad):
                    QMessageBox.warning(self, "Error", "No hay suficiente stock para eliminar la cantidad especificada.")
                    return

                # Reducir la cantidad o eliminar el producto si la cantidad llega a 0
                nuevo_stock = stock_actual - int(cantidad)
                if nuevo_stock > 0:
                    cursor.execute("""
                        UPDATE inventario SET cantStock = %s
                        WHERE idProducto IN (SELECT idProducto FROM productos WHERE codProducto = %s) AND idSucursal = %s
                    """, (nuevo_stock, codigo, self.sucursal_id))
                    QMessageBox.information(self, "Éxito", "Cantidad eliminada exitosamente.")
                else:
                    # Eliminar el producto del inventario y de la tabla productos si el stock llega a 0
                    cursor.execute("""
                        DELETE FROM inventario WHERE idProducto IN (SELECT idProducto FROM productos WHERE codProducto = %s) AND idSucursal = %s
                    """, (codigo, self.sucursal_id))
                    cursor.execute("DELETE FROM productos WHERE codProducto = %s", (codigo,))
                    QMessageBox.information(self, "Éxito", "Producto eliminado completamente de la base de datos.")

            conn.commit()
            cursor.close()
            conn.close()
            dialog.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def ver_inventario_cocina(self):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT p.codProducto, p.nProducto, p.valor, c.cantStock, cat.nCategoria
                FROM productos p
                JOIN casino c ON p.idProducto = c.idProducto
                LEFT JOIN categorias cat ON p.idCategoria = cat.idCategoria
                WHERE c.idSucursal = %s
            """, (self.sucursal_id,))
            productos = cursor.fetchall()

            if not productos:
                QMessageBox.information(self, "Inventario Cocina Vacío", "No hay productos en el inventario de cocina para esta sucursal.")
                return

            # Crear una ventana de diálogo para mostrar el inventario de cocina
            inventario_cocina_window = QDialog(self)
            inventario_cocina_window.setWindowTitle("Inventario de Cocina")
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
            inventario_cocina_window.setLayout(inventario_layout)
            inventario_cocina_window.setGeometry(100, 100, 700, 400)
            inventario_cocina_window.exec_()

            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo conectar a la base de datos: {str(e)}")


    def agregar_producto_cocina(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Agregar Producto a Cocina")
        form_layout = QFormLayout()

        # Campos para agregar el producto
        self.codigo_producto_input_cocina = QLineEdit()
        self.nombre_producto_input_cocina = QLineEdit()
        self.valor_producto_input_cocina = QLineEdit()
        self.cantidad_producto_input_cocina = QLineEdit()

        # Combobox para seleccionar la categoría
        self.categoria_combo_cocina = QComboBox()
        self.cargar_categorias_cocina()

        form_layout.addRow("Código del Producto:", self.codigo_producto_input_cocina)
        form_layout.addRow("Nombre del Producto:", self.nombre_producto_input_cocina)
        form_layout.addRow("Valor del Producto:", self.valor_producto_input_cocina)
        form_layout.addRow("Cantidad del Producto:", self.cantidad_producto_input_cocina)
        form_layout.addRow("Categoría:", self.categoria_combo_cocina)

        btn_guardar = QPushButton("Guardar")
        btn_guardar.clicked.connect(lambda: self.guardar_producto_cocina(dialog))
        form_layout.addRow(btn_guardar)

        dialog.setLayout(form_layout)
        dialog.exec_()

    def guardar_producto_cocina(self, dialog):
        codigo = self.codigo_producto_input_cocina.text()
        nombre = self.nombre_producto_input_cocina.text()
        valor = self.valor_producto_input_cocina.text()
        cantidad = self.cantidad_producto_input_cocina.text()

        if not codigo or not nombre or not valor or not cantidad:
            QMessageBox.warning(self, "Error", "Por favor complete todos los campos")
            return

        try:
            conn = obtener_conexion()
            cursor = conn.cursor()

            # Insertar producto si es nuevo, o actualizar el stock si ya existe en la cocina
            cursor.execute(
                "INSERT INTO productos (codProducto, nProducto, valor, idCategoria) VALUES (%s, %s, %s, %s) ON CONFLICT (codProducto) DO NOTHING RETURNING idProducto",
                (codigo, nombre, valor, self.categoria_combo_cocina.currentData())
            )
            producto = cursor.fetchone()
            if producto:
                id_producto = producto[0]
            else:
                cursor.execute("SELECT idProducto FROM productos WHERE codProducto = %s", (codigo,))
                id_producto = cursor.fetchone()[0]

            # Insertar en inventario de cocina
            cursor.execute(
                "INSERT INTO casino (idSucursal, idProducto, cantStock) VALUES (%s, %s, %s) ON CONFLICT (idSucursal, idProducto) DO UPDATE SET cantStock = casino.cantStock + EXCLUDED.cantStock",
                (self.sucursal_id, id_producto, cantidad)
            )
            conn.commit()
            QMessageBox.information(self, "Éxito", "Producto agregado exitosamente al inventario de cocina.")
            dialog.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
        finally:
            cursor.close()
            conn.close()

    def cargar_categorias_cocina(self):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute("SELECT idCategoria, nCategoria FROM categorias")
            categorias = cursor.fetchall()
            for categoria in categorias:
                self.categoria_combo_cocina.addItem(categoria[1], categoria[0])
            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar las categorías: {str(e)}")


    def eliminar_producto_cocina(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Eliminar Producto de Cocina")
        form_layout = QFormLayout()

        # Campos para seleccionar el producto y cantidad a eliminar
        self.codigo_producto_eliminar_input = QLineEdit()
        self.cantidad_producto_eliminar_input = QLineEdit()
        form_layout.addRow("Código del Producto:", self.codigo_producto_eliminar_input)
        form_layout.addRow("Cantidad a Eliminar:", self.cantidad_producto_eliminar_input)

        btn_eliminar = QPushButton("Eliminar")
        btn_eliminar.clicked.connect(lambda: self.confirmar_eliminar_producto_cocina(dialog))
        form_layout.addRow(btn_eliminar)

        dialog.setLayout(form_layout)
        dialog.exec_()

    def confirmar_eliminar_producto_cocina(self, dialog):
        codigo = self.codigo_producto_eliminar_input.text()
        cantidad = self.cantidad_producto_eliminar_input.text()

        # Validar que se ingresen los campos
        if not codigo or not cantidad.isdigit():
            QMessageBox.warning(self, "Error", "Por favor complete todos los campos correctamente.")
            return

        cantidad = int(cantidad)

        try:
            conn = obtener_conexion()
            cursor = conn.cursor()

            # Verificar si el producto existe en el inventario de cocina de la sucursal
            cursor.execute("""
                SELECT cantStock FROM casino
                WHERE idProducto = (SELECT idProducto FROM productos WHERE codProducto = %s) AND idSucursal = %s
            """, (codigo, self.sucursal_id))
            resultado = cursor.fetchone()

            if not resultado:
                QMessageBox.warning(self, "Error", "El producto no existe en el inventario de cocina de esta sucursal.")
                return

            stock_actual = resultado[0]

            # Verificar que haya suficiente stock para eliminar
            if stock_actual < cantidad:
                QMessageBox.warning(self, "Error", "No hay suficiente stock para eliminar la cantidad especificada.")
                return

            # Eliminar la cantidad especificada del inventario de cocina
            cursor.execute("""
                UPDATE casino
                SET cantStock = cantStock - %s
                WHERE idProducto = (SELECT idProducto FROM productos WHERE codProducto = %s) AND idSucursal = %s
            """, (cantidad, codigo, self.sucursal_id))

            conn.commit()
            cursor.close()
            conn.close()

            QMessageBox.information(self, "Éxito", "Producto eliminado exitosamente del inventario de cocina.")
            dialog.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo conectar a la base de datos: {str(e)}")
            
    def traspasar_producto_cocina(self):
        # Crear un diálogo para seleccionar la sucursal de origen y el producto a traspasar
        dialog = QDialog(self)
        dialog.setWindowTitle("Traspasar Producto entre Sucursales")
        form_layout = QFormLayout(dialog)

        # Seleccionar sucursal de origen
        self.sucursal_origen_combo = QComboBox()
        self.cargar_sucursales_asociadas()
        form_layout.addRow("Sucursal de Origen:", self.sucursal_origen_combo)

        # Seleccionar producto en inventario de cocina de la sucursal origen
        self.producto_origen_combo = QComboBox()
        self.sucursal_origen_combo.currentIndexChanged.connect(self.cargar_productos_origen)
        form_layout.addRow("Producto a Traspasar:", self.producto_origen_combo)

        # Campo para cantidad a traspasar
        self.cantidad_traspaso_input = QLineEdit()
        form_layout.addRow("Cantidad a Traspasar:", self.cantidad_traspaso_input)

        btn_traspasar = QPushButton("Traspasar")
        btn_traspasar.clicked.connect(lambda: self.confirmar_traspaso(dialog))
        form_layout.addRow(btn_traspasar)

        dialog.setLayout(form_layout)
        dialog.exec_()

    def cargar_sucursales_asociadas(self):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT s.idSucursal, s.nombre 
                FROM sucursal s
                JOIN us_su us ON s.idSucursal = us.idSucursal
                WHERE us.idUsuario = %s
            """, (self.usuario[0],))
            sucursales = cursor.fetchall()

            self.sucursal_origen_combo.clear()
            for sucursal in sucursales:
                self.sucursal_origen_combo.addItem(sucursal[1], sucursal[0])
                
            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar las sucursales: {str(e)}")

    def cargar_productos_origen(self):
        sucursal_id = self.sucursal_origen_combo.currentData()
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT p.idProducto, p.nProducto 
                FROM productos p
                JOIN casino c ON p.idProducto = c.idProducto
                WHERE c.idSucursal = %s
            """, (sucursal_id,))
            productos = cursor.fetchall()

            self.producto_origen_combo.clear()
            for producto in productos:
                self.producto_origen_combo.addItem(producto[1], producto[0])

            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar los productos: {str(e)}")

    def confirmar_traspaso(self, dialog):
        sucursal_origen_id = self.sucursal_origen_combo.currentData()
        producto_id = self.producto_origen_combo.currentData()
        cantidad = self.cantidad_traspaso_input.text()

        if not cantidad.isdigit() or int(cantidad) <= 0:
            QMessageBox.warning(self, "Error", "La cantidad debe ser un número positivo.")
            return

        try:
            cantidad = int(cantidad)
            conn = obtener_conexion()
            cursor = conn.cursor()

            # Reducir la cantidad en la sucursal de origen
            cursor.execute("""
                UPDATE casino
                SET cantStock = cantStock - %s
                WHERE idSucursal = %s AND idProducto = %s AND cantStock >= %s
            """, (cantidad, sucursal_origen_id, producto_id, cantidad))

            if cursor.rowcount == 0:
                QMessageBox.warning(self, "Error", "La sucursal de origen no tiene suficiente stock.")
                return

            # Aumentar la cantidad en la sucursal destino
            cursor.execute("""
                INSERT INTO casino (idSucursal, idProducto, cantStock)
                VALUES (%s, %s, %s)
                ON CONFLICT (idSucursal, idProducto)
                DO UPDATE SET cantStock = casino.cantStock + EXCLUDED.cantStock
            """, (self.sucursal_id, producto_id, cantidad))

            conn.commit()
            cursor.close()
            conn.close()
            QMessageBox.information(self, "Éxito", "Producto traspasado exitosamente.")
            dialog.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo realizar el traspaso: {str(e)}")

    def ver_estadisticas(self):
        QMessageBox.information(self, "Información", "Función para ver estadísticas aún no implementada.")






    def verificar_inventario_bajo(self):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()

            # Consulta para la tabla `inventario`
            cursor.execute("""
                SELECT p.nProducto, i.cantStock, 'Inventario' AS origen
                FROM productos p
                JOIN inventario i ON p.idProducto = i.idProducto
                WHERE i.idSucursal = %s AND i.cantStock < %s
            """, (self.sucursal_id, 5))
            productos_bajo_stock_inventario = cursor.fetchall()

            # Consulta para la tabla `casino`
            cursor.execute("""
                SELECT p.nProducto, c.cantStock, 'Cocina' AS origen
                FROM productos p
                JOIN casino c ON p.idProducto = c.idProducto
                WHERE c.idSucursal = %s AND c.cantStock < %s
            """, (self.sucursal_id, 5))
            productos_bajo_stock_cocina = cursor.fetchall()

            cursor.close()
            conn.close()

            # Combinar los resultados de ambas consultas
            productos_bajo_stock = productos_bajo_stock_inventario + productos_bajo_stock_cocina

            if productos_bajo_stock:
                # Construir mensaje de alerta
                mensaje_alerta = "Productos con bajo stock:\n"
                for producto, cantidad, origen in productos_bajo_stock:
                    mensaje_alerta += f"- {producto} (Origen: {origen}): {cantidad} unidades\n"
                
                # Mostrar alerta en la ventana de administrador
                QMessageBox.warning(self, "Alerta de Inventario Bajo", mensaje_alerta)
            else:
                print("No hay productos con bajo stock en esta sucursal.")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo verificar el inventario: {str(e)}")

    def mostrar(self):
            # Llamar a la verificación de inventario bajo al abrir la ventana
        self.verificar_inventario_bajo()
        super().show()