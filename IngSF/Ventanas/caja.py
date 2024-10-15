# ventanas/caja.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QComboBox, QMessageBox, QFormLayout, QDialog
from db import obtener_conexion

class VentanaCaja(QWidget):
    def __init__(self, sucursal_id):
        super().__init__()
        self.sucursal_id = sucursal_id  # Almacenar la sucursal seleccionada
        self.setWindowTitle("Caja - Realizar Venta")
        self.setGeometry(100, 100, 500, 400)

        # Layout principal
        layout = QVBoxLayout()

        # Barra de Búsqueda
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Buscar producto por nombre o código")
        self.search_bar.textChanged.connect(self.buscar_producto)  # Conectar al método de búsqueda
        layout.addWidget(self.search_bar)

        # Combobox para mostrar opciones de productos durante la búsqueda
        self.producto_combo = QComboBox(self)
        layout.addWidget(self.producto_combo)

        # Botón para agregar producto al carrito
        self.btn_agregar = QPushButton("Agregar al Carrito")
        self.btn_agregar.clicked.connect(self.agregar_al_carrito)
        layout.addWidget(self.btn_agregar)

        # Tabla de Carrito de Compras
        self.carrito_table = QTableWidget(self)
        self.carrito_table.setColumnCount(4)
        self.carrito_table.setHorizontalHeaderLabels(["Producto", "Cantidad", "Subtotal", "Acciones"])
        layout.addWidget(self.carrito_table)

        # Total de la Compra
        self.total_label = QLabel("Total: $0.00", self)
        layout.addWidget(self.total_label)

        # Botón para Finalizar Compra
        self.btn_finalizar = QPushButton("Finalizar Compra")
        self.btn_finalizar.clicked.connect(self.finalizar_compra)
        layout.addWidget(self.btn_finalizar)

        self.setLayout(layout)

        # Variable para el total
        self.total = 0

    def buscar_producto(self):
        # Buscar productos por código o nombre de la base de datos
        texto_busqueda = self.search_bar.text()
        if not texto_busqueda:
            self.producto_combo.clear()
            return

        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT Codigo_Producto, Nombre_Producto, Valor_Producto FROM Producto
                WHERE (Codigo_Producto ILIKE %s OR Nombre_Producto ILIKE %s)
                AND ID_Producto IN (SELECT ID_Producto FROM Inventario WHERE ID_Sucursal = %s)
            """, (f"%{texto_busqueda}%", f"%{texto_busqueda}%", self.sucursal_id))
            productos = cursor.fetchall()

            # Actualizar el combo box con las opciones encontradas
            self.producto_combo.clear()
            for producto in productos:
                codigo, nombre, valor = producto
                self.producto_combo.addItem(f"{codigo} - {nombre} ($ {valor})", (codigo, nombre, valor))

            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo realizar la búsqueda: {str(e)}")

    def agregar_al_carrito(self):
        # Obtener el producto seleccionado
        producto_seleccionado = self.producto_combo.currentData()
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
            
            subtotal = cantidad * float(valor)

            # Agregar a la tabla del carrito
            row_position = self.carrito_table.rowCount()
            self.carrito_table.insertRow(row_position)
            self.carrito_table.setItem(row_position, 0, QTableWidgetItem(nombre))
            self.carrito_table.setItem(row_position, 1, QTableWidgetItem(str(cantidad)))
            self.carrito_table.setItem(row_position, 2, QTableWidgetItem(f"$ {subtotal:.2f}"))

            # Crear botón para eliminar producto
            btn_eliminar = QPushButton("Eliminar")
            btn_eliminar.clicked.connect(lambda: self.eliminar_producto(row_position))
            self.carrito_table.setCellWidget(row_position, 3, btn_eliminar)

            # Actualizar el total
            self.total += subtotal
            self.total_label.setText(f"Total: $ {self.total:.2f}")

            dialog.accept()
        except ValueError:
            QMessageBox.warning(self, "Error", "Ingrese una cantidad válida (número entero positivo).")

    def eliminar_producto(self, row_position):
        # Eliminar el producto del carrito
        subtotal = float(self.carrito_table.item(row_position, 2).text().replace('$', '').replace(',', ''))
        self.total -= subtotal  # Restar del total
        self.total_label.setText(f"Total: $ {self.total:.2f}")
        
        self.carrito_table.removeRow(row_position)

    def finalizar_compra(self):
        # Lógica para finalizar la compra y descontar inventario
        if self.carrito_table.rowCount() == 0:
            QMessageBox.warning(self, "Error", "El carrito está vacío.")
            return

        try:
            conn = obtener_conexion()
            cursor = conn.cursor()

            # Descontar cada producto en el inventario
            for row in range(self.carrito_table.rowCount()):
                nombre = self.carrito_table.item(row, 0).text()
                cantidad = int(self.carrito_table.item(row, 1).text())

                cursor.execute("""
                    UPDATE Inventario SET Cantidad = Cantidad - %s
                    WHERE ID_Producto IN (
                        SELECT ID_Producto FROM Producto WHERE Nombre_Producto = %s
                    ) AND ID_Sucursal = %s
                """, (cantidad, nombre, self.sucursal_id))

            conn.commit()
            cursor.close()
            conn.close()

            QMessageBox.information(self, "Éxito", "Compra finalizada exitosamente.")
            self.reset_carrito()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo finalizar la compra: {str(e)}")

    def reset_carrito(self):
        # Reiniciar el carrito de compras y el total
        self.carrito_table.setRowCount(0)
        self.total = 0
        self.total_label.setText("Total: $0.00")
