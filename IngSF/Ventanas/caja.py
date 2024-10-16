# ventanas/caja.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QComboBox, QMessageBox, QFormLayout, QDialog
from PyQt5.QtCore import QTimer
from decimal import Decimal
from boleta import BoletaPDF
from db import obtener_conexion

class VentanaCaja(QWidget):
    def __init__(self, sucursal_id):
        super().__init__()
        self.sucursal_id = sucursal_id  # Almacenar la sucursal seleccionada
        self.setWindowTitle("Caja - Realizar Venta")
        self.setGeometry(100, 100, 600, 600)

        # Cargar inventario en memoria
        self.productos_inventario = self.cargar_inventario()
        self.total = Decimal(0)  # Asegúrate de que total sea un Decimal

        # Layout principal
        layout = QVBoxLayout()

        # Barra de búsqueda por nombre
        self.search_name_bar = QLineEdit(self)
        self.search_name_bar.setPlaceholderText("Buscar producto por nombre")
        self.search_name_bar.textChanged.connect(self.iniciar_busqueda_nombre)
        layout.addWidget(self.search_name_bar)

        # Combobox para mostrar productos por nombre
        self.producto_nombre_combo = QComboBox(self)
        self.producto_nombre_combo.activated.connect(self.agregar_al_carrito_nombre)
        layout.addWidget(self.producto_nombre_combo)

        # Barra de búsqueda por código
        self.search_code_bar = QLineEdit(self)
        self.search_code_bar.setPlaceholderText("Buscar producto por código")
        self.search_code_bar.textChanged.connect(self.iniciar_busqueda_codigo)
        layout.addWidget(self.search_code_bar)

        # Combobox para mostrar productos por código
        self.producto_codigo_combo = QComboBox(self)
        self.producto_codigo_combo.activated.connect(self.agregar_al_carrito_codigo)
        layout.addWidget(self.producto_codigo_combo)

        # Tabla de Carrito de Compras
        self.carrito_table = QTableWidget(self)
        self.carrito_table.setColumnCount(4)
        self.carrito_table.setHorizontalHeaderLabels(["Producto", "Cantidad", "Subtotal", "Eliminar"])
        layout.addWidget(self.carrito_table)

        # Seleccionar método de pago
        self.metodo_pago_combo = QComboBox(self)
        self.cargar_metodos_pago()
        layout.addWidget(QLabel("Seleccionar método de pago:"))
        layout.addWidget(self.metodo_pago_combo)

        # Total de la Compra
        self.total_label = QLabel("Total: $0.00", self)
        layout.addWidget(self.total_label)

        # Botón para Finalizar Compra
        self.btn_finalizar = QPushButton("Finalizar Compra", self)
        self.btn_finalizar.clicked.connect(self.finalizar_compra)
        layout.addWidget(self.btn_finalizar)

        self.setLayout(layout)

        # Timers para las búsquedas con retraso
        self.timer_nombre = QTimer(self)
        self.timer_nombre.setSingleShot(True)
        self.timer_nombre.timeout.connect(self.buscar_producto_nombre)

        self.timer_codigo = QTimer(self)
        self.timer_codigo.setSingleShot(True)
        self.timer_codigo.timeout.connect(self.buscar_producto_codigo)


    def cargar_inventario(self):
        # Cargar el inventario de la sucursal al iniciar la ventana
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT p.ID_Producto, p.Codigo_Producto, p.Nombre_Producto, i.Cantidad, p.Valor_Producto
                FROM Producto p
                JOIN Inventario i ON p.ID_Producto = i.ID_Producto
                WHERE i.ID_Sucursal = %s
            """, (self.sucursal_id,))
            productos = cursor.fetchall()
            cursor.close()
            conn.close()
            return productos
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar el inventario: {str(e)}")
            return []

    def cargar_metodos_pago(self):
        # Cargar los métodos de pago desde la base de datos
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute("SELECT id_metodo, nombre_metodo FROM metodo_pago")
            metodos = cursor.fetchall()

            for metodo in metodos:
                self.metodo_pago_combo.addItem(metodo[1], metodo[0])

            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar los métodos de pago: {str(e)}")

    def iniciar_busqueda_nombre(self):
        # Reiniciar el temporizador para la búsqueda por nombre
        self.timer_nombre.start(300)

    def iniciar_busqueda_codigo(self):
        # Reiniciar el temporizador para la búsqueda por código
        self.timer_codigo.start(300)

    def buscar_producto_nombre(self):
        # Filtrar productos en memoria por nombre
        texto_busqueda = self.search_name_bar.text().lower()
        if not texto_busqueda:
            self.producto_nombre_combo.clear()
            return

        # Filtrar la lista de productos por nombre
        productos_filtrados = [producto for producto in self.productos_inventario if texto_busqueda in producto[2].lower()]

        # Actualizar el combo box con los resultados
        self.producto_nombre_combo.clear()
        for producto in productos_filtrados:
            codigo, nombre, valor = producto[1], producto[2], producto[4]
            self.producto_nombre_combo.addItem(f"{nombre} - ($ {valor})", (codigo, nombre, valor))

    def buscar_producto_codigo(self):
        # Filtrar productos en memoria por código
        texto_busqueda = self.search_code_bar.text().lower()
        if not texto_busqueda:
            self.producto_codigo_combo.clear()
            return

        # Filtrar la lista de productos por código
        productos_filtrados = [producto for producto in self.productos_inventario if texto_busqueda in producto[1].lower()]

        # Actualizar el combo box con los resultados
        self.producto_codigo_combo.clear()
        for producto in productos_filtrados:
            codigo, nombre, valor = producto[1], producto[2], producto[4]
            self.producto_codigo_combo.addItem(f"{codigo} - {nombre} ($ {valor})", (codigo, nombre, valor))

    def agregar_al_carrito_nombre(self):
        # Obtener producto seleccionado por nombre
        producto_seleccionado = self.producto_nombre_combo.currentData()
        self.agregar_al_carrito(producto_seleccionado)

    def agregar_al_carrito_codigo(self):
        # Obtener producto seleccionado por código
        producto_seleccionado = self.producto_codigo_combo.currentData()
        self.agregar_al_carrito(producto_seleccionado)

    def agregar_al_carrito(self, producto_seleccionado):
        if not producto_seleccionado:
            QMessageBox.warning(self, "Error", "Seleccione un producto válido.")
            return

        codigo, nombre, valor = producto_seleccionado

        # Mostrar un diálogo para ingresar la cantidad
        dialog = QDialog(self)
        dialog.setWindowTitle("Ingresar Cantidad")
        form_layout = QFormLayout(dialog)

        cantidad_input = QLineEdit()
        form_layout.addRow("Cantidad:", cantidad_input)

        btn_aceptar = QPushButton("Aceptar")
        btn_aceptar.clicked.connect(lambda: self.confirmar_agregar_carrito(codigo, nombre, valor, cantidad_input.text(), dialog))
        form_layout.addWidget(btn_aceptar)

        dialog.setLayout(form_layout)
        dialog.exec_()

    def confirmar_agregar_carrito(self, codigo, nombre, valor, cantidad_texto, dialog):
        # Validar e intentar agregar la cantidad al carrito
        try:
            cantidad = int(cantidad_texto)
            if cantidad <= 0:
                raise ValueError("La cantidad debe ser mayor a cero.")
            
            subtotal = cantidad * valor

            # Agregar a la tabla del carrito
            row_position = self.carrito_table.rowCount()
            self.carrito_table.insertRow(row_position)
            self.carrito_table.setItem(row_position, 0, QTableWidgetItem(nombre))
            self.carrito_table.setItem(row_position, 1, QTableWidgetItem(str(cantidad)))
            self.carrito_table.setItem(row_position, 2, QTableWidgetItem(f"$ {subtotal:.2f}"))

            # Botón para eliminar producto con la fila capturada
            btn_eliminar = QPushButton("Eliminar")
            btn_eliminar.clicked.connect(lambda: self.eliminar_del_carrito(row_position))
            self.carrito_table.setCellWidget(row_position, 3, btn_eliminar)

            # Actualizar el total
            self.total += subtotal
            self.total_label.setText(f"Total: $ {self.total:.2f}")

            dialog.accept()

            # Actualizar los botones "Eliminar" después de agregar un nuevo producto
            self.actualizar_botones_eliminar()
        except ValueError:
            QMessageBox.warning(self, "Error", "Ingrese una cantidad válida (número entero positivo).")

    def eliminar_del_carrito(self, row):
        try:
            # Verificar si la fila es válida antes de eliminar
            if row < 0 or row >= self.carrito_table.rowCount():
                QMessageBox.warning(self, "Error", "No se pudo eliminar el producto, la fila seleccionada no es válida.")
                return

            # Obtener el subtotal de la fila a eliminar y convertirlo a Decimal
            subtotal = Decimal(self.carrito_table.item(row, 2).text().replace("$", "").strip())

            # Restar el subtotal del total general
            self.total -= subtotal
            if self.total < 0:
                self.total = Decimal(0)  # Asegurarse de que no sea negativo
            self.total_label.setText(f"Total: $ {self.total:.2f}")

            # Eliminar la fila del carrito
            self.carrito_table.removeRow(row)

            # Si el carrito está vacío, actualizar el total a $0.00
            if self.carrito_table.rowCount() == 0:
                self.total = Decimal(0)
                self.total_label.setText("Total: $ 0.00")

            # Actualizar los botones "Eliminar" después de eliminar un producto
            self.actualizar_botones_eliminar()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error al eliminar el producto del carrito: {str(e)}")

    def actualizar_botones_eliminar(self):
        # Actualizar los botones "Eliminar" para todas las filas después de cualquier cambio
        for row in range(self.carrito_table.rowCount()):
            btn_eliminar = QPushButton("Eliminar")
            btn_eliminar.clicked.connect(lambda _, row=row: self.eliminar_del_carrito(row))
            self.carrito_table.setCellWidget(row, 3, btn_eliminar)


    def finalizar_compra(self):
        # Lógica para finalizar la compra y registrar en la base de datos
        if self.carrito_table.rowCount() == 0:
            QMessageBox.warning(self, "Error", "El carrito está vacío.")
            return

        id_metodo_pago = self.metodo_pago_combo.currentData()

        try:
            conn = obtener_conexion()
            cursor = conn.cursor()

            # Registrar la venta en la tabla "venta"
            cursor.execute("""
                INSERT INTO Venta (fecha_venta, id_sucursal, id_metodo, total_venta)
                VALUES (CURRENT_DATE, %s, %s, %s) RETURNING id_venta
            """, (self.sucursal_id, id_metodo_pago, self.total))
            id_venta = cursor.fetchone()[0]  # Obtener el ID de la venta recién creada

            # Recorrer el carrito y registrar en "detalle_venta" y actualizar inventario
            for row in range(self.carrito_table.rowCount()):
                nombre = self.carrito_table.item(row, 0).text()
                cantidad = int(self.carrito_table.item(row, 1).text())
                subtotal = float(self.carrito_table.item(row, 2).text().replace("$", "").strip())

                # Obtener el ID del producto
                cursor.execute("""
                    SELECT ID_Producto FROM Producto WHERE Nombre_Producto = %s
                """, (nombre,))
                id_producto = cursor.fetchone()[0]

                # Registrar el detalle de la venta
                cursor.execute("""
                    INSERT INTO Detalle_Venta (id_venta, id_producto, cantidad_vendida, subtotal)
                    VALUES (%s, %s, %s, %s)
                """, (id_venta, id_producto, cantidad, subtotal))

                # Actualizar el inventario en la base de datos
                cursor.execute("""
                    UPDATE Inventario SET Cantidad = Cantidad - %s
                    WHERE ID_Producto = %s AND ID_Sucursal = %s
                """, (cantidad, id_producto, self.sucursal_id))

                # Actualizar la cantidad en `self.productos_inventario`
                for producto in self.productos_inventario:
                    if producto[0] == id_producto:
                        producto[3] -= cantidad
                        break

            conn.commit()
            cursor.close()
            conn.close()

            # Generar la boleta usando la clase BoletaPDF
            boleta = BoletaPDF(id_venta, self.total)
            output_path = boleta.generar_boleta()

            if output_path:
                QMessageBox.information(self, "Éxito", f"Compra finalizada y boleta generada exitosamente.\nBoleta: {output_path}")

            self.reset_carrito()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo finalizar la compra: {str(e)}")

    def reset_carrito(self):
        # Reiniciar el carrito de compras y el total
        self.carrito_table.setRowCount(0)
        self.total = Decimal(0)
        self.total_label.setText("Total: $0.00")

