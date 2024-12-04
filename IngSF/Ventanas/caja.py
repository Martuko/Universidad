# ventanas/caja.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QComboBox, QMessageBox, QFormLayout, QDialog, QHBoxLayout, QHeaderView
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from decimal import Decimal
from boleta import BoletaPDF
from db import obtener_conexion
from utils import ruta_recurso
class VentanaCaja(QWidget):
    def __init__(self, usuario,sucursal_id, ventana_anterior=None):
        super().__init__()
        self.usuario = usuario
        self.sucursal_id = sucursal_id  # Almacenar la sucursal seleccionada
        self.setWindowTitle("Caja - Realizar Venta")
        self.setGeometry(100, 100, 600, 600)
        self.ventana_anterior = ventana_anterior

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

        # Ajustar el ancho de las columnas
        self.carrito_table.setColumnWidth(0, 200)  # Columna "Producto"
        self.carrito_table.setColumnWidth(1, 100)  # Columna "Cantidad"
        self.carrito_table.setColumnWidth(2, 120)  # Columna "Subtotal"
        self.carrito_table.setColumnWidth(3, 100)  # Columna "Eliminar"

        # Opcional: ajustar altura de las filas
        self.carrito_table.verticalHeader().setDefaultSectionSize(50)  # Altura de las filas
        self.carrito_table.horizontalHeader().setStretchLastSection(False)  # No expandir última columna

        # Ajustar automáticamente el tamaño de las columnas al contenido (opcional)
        self.carrito_table.resizeColumnsToContents()

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

        btn_cerrar_caja = QPushButton("Cerrar Caja")
        btn_cerrar_caja.clicked.connect(self.abrir_cierre_caja)
        layout.addWidget(btn_cerrar_caja)

        if self.ventana_anterior:
            btn_regresar = QPushButton("Regresar")
            btn_regresar.clicked.connect(self.verificar_clave_para_regresar)
            layout.addWidget(btn_regresar)
        # Botón para Cancelar Compra
        self.setLayout(layout)

        # Timers para las búsquedas con retraso
        self.timer_nombre = QTimer(self)
        self.timer_nombre.setSingleShot(True)
        self.timer_nombre.timeout.connect(self.buscar_producto_nombre)

        self.timer_codigo = QTimer(self)
        self.timer_codigo.setSingleShot(True)
        self.timer_codigo.timeout.connect(self.buscar_producto_codigo)


    def verificar_clave_para_regresar(self):
        # Crear un diálogo para ingresar la clave
        dialogo_clave = QDialog(self)
        dialogo_clave.setWindowTitle("Confirmar Clave")
        form_layout = QFormLayout(dialogo_clave)

        # Campo para ingresar la clave
        clave_input = QLineEdit()
        clave_input.setEchoMode(QLineEdit.Password)
        form_layout.addRow("Ingrese su clave:", clave_input)

        # Botón de confirmar
        btn_confirmar = QPushButton("Confirmar")
        btn_confirmar.clicked.connect(lambda: self.confirmar_clave(clave_input.text(), dialogo_clave))
        form_layout.addWidget(btn_confirmar)

        dialogo_clave.setLayout(form_layout)
        dialogo_clave.exec_()

    def confirmar_clave(self, clave_ingresada, dialogo):
        try:
            # Conectar a la base de datos y verificar la clave
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute("SELECT password FROM usuario WHERE username = %s", (self.usuario[1],))
            clave_real = cursor.fetchone()
            cursor.close()
            conn.close()

            # Comprobar si la clave ingresada coincide con la clave real
            if clave_real and clave_real[0] == clave_ingresada:
                if self.ventana_anterior:
                    self.ventana_anterior.show()
                self.close()
                dialogo.accept()
            else:
                QMessageBox.warning(self, "Error", "Clave incorrecta.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo conectar a la base de datos: {str(e)}")

    def cargar_inventario(self):
        # Cargar el inventario de la sucursal al iniciar la ventana
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT p.idProducto, p.codProducto, p.nProducto, i.cantStock, p.valor
                FROM productos p
                JOIN inventario i ON p.idProducto = i.idProducto
                WHERE i.idSucursal = %s
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
            cursor.execute("SELECT idMetodo, nMetodo FROM metodopago")
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

            # Crear un botón de eliminación con ícono
            btn_eliminar = QPushButton()
            try:
                icon_path = ruta_recurso("Recursos/Eliminar.png")
                print(f"Ruta del ícono: {icon_path}")

                btn_eliminar.setIcon(QIcon(icon_path))
                btn_eliminar.setIconSize(QSize(32, 32))
            except Exception as e:
                print(f"Error al cargar el ícono: {e}")
                btn_eliminar.setText("Eliminar")  # Texto de respaldo si no hay ícono
            btn_eliminar.setStyleSheet("border: none;")  # Opcional
            btn_eliminar.clicked.connect(lambda: self.eliminar_del_carrito(row_position))
            self.carrito_table.setCellWidget(row_position, 3, btn_eliminar)


                # Ajustar el tamaño de la fila y la columna
            self.carrito_table.setRowHeight(row_position, 40)
            self.carrito_table.setColumnWidth(3, 100)

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
        if self.carrito_table.rowCount() == 0:
            QMessageBox.warning(self, "Error", "El carrito está vacío.")
            return

        id_metodo_pago = self.metodo_pago_combo.currentData()

        try:
            conn = obtener_conexion()
            cursor = conn.cursor()

            # Registrar la venta en la tabla "ventas"
            cursor.execute("""
                INSERT INTO ventas (fecha, idSucursal, idMetodo, totalVenta)
                VALUES (CURRENT_TIMESTAMP, %s, %s, %s) RETURNING idVentas
            """, (self.sucursal_id, id_metodo_pago, self.total))

            resultado = cursor.fetchone()
            if resultado is None:
                QMessageBox.critical(self, "Error", "No se pudo obtener el ID de la venta.")
                return
            id_venta = resultado[0]

            for row in range(self.carrito_table.rowCount()):
                nombre = self.carrito_table.item(row, 0).text()
                cantidad = int(self.carrito_table.item(row, 1).text())
                subtotal = float(self.carrito_table.item(row, 2).text().replace("$", "").strip())

                # Obtener el ID del producto
                cursor.execute("SELECT idProducto FROM productos WHERE nProducto = %s", (nombre,))
                producto_resultado = cursor.fetchone()
                if producto_resultado is None:
                    QMessageBox.critical(self, "Error", f"No se pudo encontrar el producto '{nombre}' en la base de datos.")
                    return
                id_producto = producto_resultado[0]

                # Registrar el detalle de la venta
                cursor.execute("""
                    INSERT INTO ventadetalle (idVentas, idProducto, cantidad_vendida, subTotal)
                    VALUES (%s, %s, %s, %s)
                """, (id_venta, id_producto, cantidad, subtotal))

                # Actualizar o eliminar el inventario según la cantidad
                cursor.execute("SELECT cantStock FROM inventario WHERE idProducto = %s AND idSucursal = %s", (id_producto, self.sucursal_id))
                stock_resultado = cursor.fetchone()
                if stock_resultado is None:
                    QMessageBox.critical(self, "Error", f"No se encontró inventario para el producto '{nombre}' en la sucursal seleccionada.")
                    return
                stock_actual = stock_resultado[0]

                if stock_actual - cantidad > 0:
                    cursor.execute("""
                        UPDATE inventario SET cantStock = cantStock - %s
                        WHERE idProducto = %s AND idSucursal = %s
                    """, (cantidad, id_producto, self.sucursal_id))
                else:
                    cursor.execute("""
                        DELETE FROM inventario
                        WHERE idProducto = %s AND idSucursal = %s
                    """, (id_producto, self.sucursal_id))

            conn.commit()
            cursor.close()
            conn.close()

            # Generar la boleta y reiniciar el carrito
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
    def abrir_cierre_caja(self):
        # Ventana emergente para el cierre de caja
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Cierre de Caja")

        # Calcular totales del día
        total_ventas, productos_vendidos = self.calcular_totales_dia()

        # Layout para mostrar los totales del cierre
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Total en dinero vendido: $ {total_ventas:.2f}"))
        layout.addWidget(QLabel(f"Cantidad de productos vendidos: {productos_vendidos}"))

        # Formulario para ventas manuales
        form_layout = QFormLayout()
        producto_input = QLineEdit()
        cantidad_input = QLineEdit()
        form_layout.addRow("Producto o Código:", producto_input)
        form_layout.addRow("Cantidad Vendida:", cantidad_input)

        # Botones
        btn_agregar_venta = QPushButton("Agregar Venta Manual")
        btn_agregar_venta.clicked.connect(
            lambda: self.agregar_venta_manual(producto_input.text(), cantidad_input.text(), total_ventas, productos_vendidos, dialog)
        )
        layout.addLayout(form_layout)
        layout.addWidget(btn_agregar_venta)

        btn_confirmar_cierre = QPushButton("Confirmar Cierre de Caja")
        btn_confirmar_cierre.clicked.connect(lambda: self.confirmar_cierre_caja(total_ventas, productos_vendidos, dialog))
        layout.addWidget(btn_confirmar_cierre)

        dialog.setLayout(layout)
        dialog.exec_()

    def agregar_venta_manual(self, producto, cantidad, total_ventas, productos_vendidos, dialog):
        try:
            cantidad = int(cantidad)

            # Verificar si el producto existe
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT idProducto, valor FROM productos
                WHERE codProducto = %s OR nProducto = %s
            """, (producto, producto))

            resultado = cursor.fetchone()

            if not resultado:
                QMessageBox.warning(self, "Error", "Producto no encontrado.")
                return

            id_producto, valor_producto = resultado
            subtotal = valor_producto * cantidad

            # Registrar la venta manual en la base de datos
            cursor.execute("""
                INSERT INTO ventas (fecha, idSucursal, idMetodo, totalVenta)
                VALUES (CURRENT_TIMESTAMP, %s, NULL, %s) RETURNING idVentas
            """, (self.sucursal_id, subtotal))

            id_venta = cursor.fetchone()[0]

            # Registrar el detalle de la venta manual
            cursor.execute("""
                INSERT INTO Detalle_Venta (id_venta, id_producto, cantidad_vendida, subtotal)
                VALUES (%s, %s, %s, %s)
            """, (id_venta, id_producto, cantidad, subtotal))

            # Actualizar el inventario
            cursor.execute("""
                UPDATE Inventario SET Cantidad = Cantidad - %s
                WHERE ID_Producto = %s AND ID_Sucursal = %s
            """, (cantidad, id_producto, self.sucursal_id))

            # Actualizar totales del cierre
            total_ventas += subtotal
            productos_vendidos += cantidad

            conn.commit()
            cursor.close()
            conn.close()

            QMessageBox.information(self, "Éxito", f"Venta manual agregada: {cantidad} x {producto}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error: {str(e)}")

    def confirmar_cierre_caja(self, total_ventas, productos_vendidos, dialog):
        try:
            # Registrar el cierre de caja en la base de datos
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Cierre_Caja (id_sucursal, fecha_cierre, total_ventas, productos_vendidos)
                VALUES (%s, CURRENT_DATE, %s, %s)
            """, (self.sucursal_id, total_ventas, productos_vendidos))

            conn.commit()
            cursor.close()
            conn.close()

            QMessageBox.information(self, "Éxito", "Cierre de caja confirmado.")
            self.reset_caja()  # Limpiar datos cargados
            dialog.accept()  # Cerrar ventana emergente
            self.cerrar_sesion()  # Volver a inicio de sesión

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo confirmar el cierre de caja: {str(e)}")

    def calcular_totales_dia(self):
        try:
            # Conectar a la base de datos
            conn = obtener_conexion()
            cursor = conn.cursor()

            # Calcular el total de dinero recaudado del día desde la tabla `ventadetalle`
            cursor.execute("""
                SELECT SUM(subtotal) FROM ventadetalle dv
                JOIN ventas v ON dv.idventas = v.idventas
                WHERE DATE(v.fecha) = CURRENT_DATE AND v.idsucursal = %s
            """, (self.sucursal_id,))

            total_dinero = cursor.fetchone()[0] or 0  # Asegurarse de que no sea None

            # Calcular la cantidad total de productos vendidos del día
            cursor.execute("""
                SELECT SUM(cantidad_vendida) FROM ventadetalle dv
                JOIN ventas v ON dv.idventas = v.idventas
                WHERE DATE(v.fecha) = CURRENT_DATE AND v.idsucursal = %s
            """, (self.sucursal_id,))
            
            productos_vendidos = cursor.fetchone()[0] or 0  # Asegurarse de que no sea None

            cursor.close()
            conn.close()

            return total_dinero, productos_vendidos

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron calcular los totales: {str(e)}")
            return 0, 0  # Devolver 0 si ocurre algún error

    def reset_caja(self):
        # Limpiar los datos cargados en memoria
        self.productos_inventario = []

    def cerrar_sesion(self):
        # Volver a la ventana de inicio de sesión
        from Ventanas.inicio_sesion import VentanaInicio
        self.inicio_sesion = VentanaInicio()
        self.inicio_sesion.show()
        self.close()