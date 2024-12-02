# ventanas/administrador.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QMessageBox, QDialog, QFormLayout, QLineEdit, QComboBox, QCheckBox, QHBoxLayout, QTabWidget, QStackedLayout, QScrollArea,QCalendarWidget
from db import obtener_conexion
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import random
import os
class VentanaAdministrador(QWidget):
    def __init__(self, usuario, sucursal_id, ventana_anterior=None):
        super().__init__()
        self.usuario = usuario
        self.sucursal_id = sucursal_id
        self.ventana_anterior = ventana_anterior

        # Configuración de la ventana
        self.setWindowTitle("Administrador - Gestión de Inventario")
        self.setGeometry(100, 100, 1200, 700)

        # Layout principal (vertical)
        layout_principal = QVBoxLayout(self)

        # --- Encabezado Superior ---
        encabezado_layout = QHBoxLayout()
        encabezado_layout.setContentsMargins(10, 10, 10, 10)

        # Logo
        base_dir = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(base_dir, "../Recursos/logo.png")
        logo_label = QLabel()
        if os.path.exists(logo_path):  # Verifica si el archivo existe
            pixmap = QPixmap(logo_path).scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(pixmap)
        else:
            logo_label.setText("Logo no encontrado")
        logo_label.setStyleSheet("background-color: transparent; border: none; margin-left: 10px;")
        encabezado_layout.addWidget(logo_label)

        # Espaciador entre el logo y el selector de sucursal
        encabezado_layout.addStretch()

        # Sucursal Seleccionada (ComboBox)
        self.sucursal_label = QLabel("Sucursal:")
        self.sucursal_label.setAlignment(Qt.AlignCenter)
        self.sucursal_label.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #000000;
            background-color: transparent;
            margin-right: 5px;
        """)

        self.sucursal_combo = QComboBox()
        self.sucursal_combo.setStyleSheet("""
            QComboBox {
                padding: 6px;
                font-size: 14px;
                border-radius: 10px;
                border: 1px solid #d3b38c;
                background-color: transparent;
                color: #000000;
                min-width: 150px;
            }
            QComboBox::drop-down {
                width: 25px;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #d3b38c;
                background-color: rgba(255, 255, 255, 0.9);
                selection-background-color: #d3b38c;
                selection-color: black;
            }
        """)

        # Cargar sucursales y manejar posibles errores
        self.cargar_sucursales()

        # Validar que haya sucursales cargadas
        if self.obtener_nombre_sucursal():
            self.sucursal_combo.setCurrentText(self.obtener_nombre_sucursal())
        else:
            self.sucursal_combo.setCurrentIndex(-1)

        self.sucursal_combo.currentIndexChanged.connect(self.cambiar_sucursal)
        encabezado_layout.addWidget(self.sucursal_label)
        encabezado_layout.addWidget(self.sucursal_combo)

        # Espaciador entre el selector de sucursal y los botones de la derecha
        encabezado_layout.addStretch()

        # Botón "Calendario"
        btn_calendario = QPushButton("Calendario")
        btn_calendario.clicked.connect(self.mostrar_calendario)
        btn_calendario.setStyleSheet("""
            QPushButton {
                background-color: #a67c52;
                color: white;
                border-radius: 10px;
                padding: 10px 20px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #8b5e3c;
            }
        """)
        encabezado_layout.addWidget(btn_calendario)  # Agregar el botón al layout del encabezado


        # Botón "Ver Estadísticas"
        btn_estadisticas = QPushButton("Ver Estadísticas")
        btn_estadisticas.clicked.connect(self.ver_estadisticas)
        btn_estadisticas.setStyleSheet("""
            QPushButton {
                background-color: #a67c52;
                color: white;
                border-radius: 10px;
                padding: 10px 20px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #8b5e3c;
            }
        """)
        encabezado_layout.addWidget(btn_estadisticas)

        # Botón "Regresar"
        btn_regresar = QPushButton("Regresar")
        btn_regresar.clicked.connect(self.regresar)
        btn_regresar.setStyleSheet("""
            QPushButton {
                background-color: #a67c52;
                color: white;
                border-radius: 10px;
                padding: 10px 20px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #8b5e3c;
            }
        """)
        encabezado_layout.addWidget(btn_regresar)

        # Agregar el encabezado al layout principal
        encabezado_widget = QWidget()
        encabezado_widget.setLayout(encabezado_layout)
        encabezado_widget.setFixedHeight(100)
        layout_principal.addWidget(encabezado_widget)

        # --- Menú Lateral Izquierdo ---
        menu_layout = QVBoxLayout()
        menu_layout.setContentsMargins(10, 10, 10, 10)

        # Tabs para "Cocina" y "Casino"
        self.tabs_menu = QTabWidget()
        self.tabs_menu.setFixedWidth(300)

        # Tab "Casino"
        tab_casino = QWidget()
        casino_layout = QVBoxLayout()
        casino_layout.setSpacing(10)

        casino_buttons = [
            ("Ver Inventario", self.ver_inventario),
            ("Agregar Producto", self.agregar_producto),
            ("Eliminar Producto", self.eliminar_producto),
        ]

        for btn_text, btn_function in casino_buttons:
            btn = QPushButton(btn_text)
            btn.setFixedHeight(40)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #a67c52;
                    color: white;
                    border-radius: 10px;
                    padding: 10px 20px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #8b5e3c;
                }
            """)
            btn.clicked.connect(btn_function)
            casino_layout.addWidget(btn)

        tab_casino.setLayout(casino_layout)
        self.tabs_menu.addTab(tab_casino, "Casino")

        # Tab "Cocina"
        tab_cocina = QWidget()
        cocina_layout = QVBoxLayout()
        cocina_layout.setSpacing(10)

        cocina_buttons = [
            ("Ver Inventario Cocina", self.ver_inventario_cocina),
            ("Agregar Producto a Cocina", self.agregar_producto_cocina),
            ("Eliminar Producto de Cocina", self.eliminar_producto_cocina),
            ("Traspasar Producto entre Sucursales", self.traspasar_producto_cocina),
        ]

        for btn_text, btn_function in cocina_buttons:  # Descomponer la tupla en texto y función
            btn = QPushButton(btn_text)  # Usar solo el texto para crear el botón
            btn.setFixedHeight(40)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #a67c52;
                    color: white;
                    border-radius: 10px;
                    padding: 10px 20px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #8b5e3c;
                }
            """)
            btn.clicked.connect(btn_function)  # Conectar la función correspondiente
            cocina_layout.addWidget(btn)

        tab_cocina.setLayout(cocina_layout)
        self.tabs_menu.addTab(tab_cocina, "Cocina")


        # Agregar el menú al layout
        menu_layout.addWidget(self.tabs_menu)

        # --- Área Principal Derecha ---
        self.area_principal_layout = QVBoxLayout()
        label_bienvenida = QLabel("Selecciona una opción del menú")
        label_bienvenida.setAlignment(Qt.AlignCenter)
        label_bienvenida.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #000000;
            background-color: transparent;
        """)
        self.area_principal_layout.addWidget(label_bienvenida)

        # Layout principal horizontal (dividir en menú y contenido)
        layout_horizontal = QHBoxLayout()
        layout_horizontal.addLayout(menu_layout)
        layout_horizontal.addLayout(self.area_principal_layout)
        layout_principal.addLayout(layout_horizontal)

        # Establecer layout principal
        self.setLayout(layout_principal)



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
        try:
            # Cambiar la sucursal seleccionada
            self.sucursal_id = self.sucursal_combo.currentData()

            # Validar que se haya seleccionado una sucursal
            if not self.sucursal_id:
                QMessageBox.warning(self, "Advertencia", "Por favor selecciona una sucursal válida.")
                return

            # Limpia el área principal
            self.limpiar_area_principal()

            # Actualiza los datos de la sucursal seleccionada
            self.actualizar_datos_sucursal()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron actualizar los datos de la sucursal: {str(e)}")

    def actualizar_datos_sucursal(self):
        try:
            # Actualizar la etiqueta con el nombre de la sucursal seleccionada
            nombre_sucursal = self.obtener_nombre_sucursal()
            self.sucursal_label.setText(f"Sucursal seleccionada: {nombre_sucursal}")

            # Agregar un mensaje inicial al área principal
            label_bienvenida = QLabel(f"Bienvenido a la sucursal {nombre_sucursal}")
            label_bienvenida.setAlignment(Qt.AlignCenter)
            label_bienvenida.setStyleSheet("""
                font-size: 18px;
                font-weight: bold;
                color: #000000;
                background-color: transparent;
            """)
            self.area_principal_layout.addWidget(label_bienvenida)

            # Puedes agregar otras actualizaciones específicas aquí, como verificar inventarios bajos
            self.verificar_inventario_bajo()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron actualizar los datos de la sucursal: {str(e)}")

    def limpiar_area_principal(self):
        """
        Limpia todos los widgets del área principal sin afectar otros layouts o widgets.
        """
        for i in reversed(range(self.area_principal_layout.count())):
            widget = self.area_principal_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()



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
    # Limpiar el área principal antes de mostrar el inventario
        for i in reversed(range(self.area_principal_layout.count())):
            widget = self.area_principal_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

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
                mensaje = QLabel("No hay productos en el inventario para esta sucursal.")
                mensaje.setAlignment(Qt.AlignCenter)
                mensaje.setStyleSheet("font-size: 16px; color: #a67c52; font-weight: bold;")
                self.area_principal_layout.addWidget(mensaje)
                return

            # Crear tabla para mostrar inventario
            inventario_table = QTableWidget()
            inventario_table.setColumnCount(5)
            inventario_table.setHorizontalHeaderLabels(["Código", "Nombre", "Valor", "Cantidad", "Categoría"])
            inventario_table.setRowCount(len(productos))

            # Estilo para la tabla
            inventario_table.setStyleSheet("""
                QTableWidget {
                    background-color: rgba(255, 255, 255, 0.9);
                    border: 1px solid #b28a68; /* Borde suave */
                    font-size: 14px;
                    color: #000;
                }
                QHeaderView::section {
                    background-color: #a67c52; /* Fondo oscuro para encabezados */
                    color: white;
                    font-size: 14px;
                    font-weight: bold;
                    border: 1px solid #8b5e3c;
                    padding: 5px;
                }
                QTableWidget::item {
                    padding: 5px;
                }
            """)

            for row, (codigo, nombre, valor, cantidad, categoria) in enumerate(productos):
                inventario_table.setItem(row, 0, QTableWidgetItem(codigo))
                inventario_table.setItem(row, 1, QTableWidgetItem(nombre))
                inventario_table.setItem(row, 2, QTableWidgetItem(f"${valor}"))
                inventario_table.setItem(row, 3, QTableWidgetItem(str(cantidad)))
                inventario_table.setItem(row, 4, QTableWidgetItem(categoria or "Sin categoría"))

            # Ajustar las columnas para que se adapten al contenido
            inventario_table.resizeColumnsToContents()

            self.area_principal_layout.addWidget(inventario_table)

            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo conectar a la base de datos: {str(e)}")



    def agregar_producto(self):
        # Limpiar el área principal antes de mostrar el formulario
        for i in reversed(range(self.area_principal_layout.count())):
            widget = self.area_principal_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Crear el formulario
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

        # Botón para guardar el producto
        btn_guardar = QPushButton("Guardar")
        btn_guardar.clicked.connect(self.guardar_producto)
        form_layout.addRow(btn_guardar)

        # Mostrar el formulario en el área principal
        widget_formulario = QWidget()
        widget_formulario.setLayout(form_layout)
        self.area_principal_layout.addWidget(widget_formulario)

        # Configurar campos según el tipo de producto
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

    def guardar_producto(self):
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

            # Refrescar el formulario
            self.agregar_producto()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def eliminar_producto(self):
        # Limpiar el área principal antes de mostrar el formulario
        for i in reversed(range(self.area_principal_layout.count())):
            widget = self.area_principal_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Crear el formulario
        form_layout = QFormLayout()

        self.codigo_producto_input = QLineEdit()
        self.cantidad_producto_input = QLineEdit()
        self.eliminar_todo_checkbox = QCheckBox("Eliminar todo el producto")

        form_layout.addRow("Código del Producto:", self.codigo_producto_input)
        form_layout.addRow("Cantidad a eliminar:", self.cantidad_producto_input)
        form_layout.addRow(self.eliminar_todo_checkbox)

        # Botón para eliminar
        btn_eliminar = QPushButton("Eliminar")
        btn_eliminar.clicked.connect(self.confirmar_eliminar_producto)
        form_layout.addRow(btn_eliminar)

        # Mostrar el formulario en el área principal
        widget_formulario = QWidget()
        widget_formulario.setLayout(form_layout)
        self.area_principal_layout.addWidget(widget_formulario)

    def confirmar_eliminar_producto(self):
        codigo = self.codigo_producto_input.text()
        cantidad = self.cantidad_producto_input.text()

        if not codigo or (not cantidad and not self.eliminar_todo_checkbox.isChecked()):
            QMessageBox.warning(self, "Error", "Por favor complete los campos necesarios.")
            return

        try:
            conn = obtener_conexion()
            cursor = conn.cursor()

            if self.eliminar_todo_checkbox.isChecked():
                cursor.execute("""
                    DELETE FROM inventario WHERE idProducto IN (SELECT idProducto FROM productos WHERE codProducto = %s) AND idSucursal = %s
                """, (codigo, self.sucursal_id))
                cursor.execute("DELETE FROM productos WHERE codProducto = %s", (codigo,))
                conn.commit()
                QMessageBox.information(self, "Éxito", "Producto eliminado completamente.")
            else:
                cursor.execute("""
                    SELECT cantStock FROM inventario
                    WHERE idProducto IN (SELECT idProducto FROM productos WHERE codProducto = %s) AND idSucursal = %s
                """, (codigo, self.sucursal_id))
                resultado = cursor.fetchone()

                if not resultado:
                    QMessageBox.warning(self, "Error", "Producto no encontrado.")
                    return

                stock_actual = resultado[0]
                if stock_actual < int(cantidad):
                    QMessageBox.warning(self, "Error", "Cantidad insuficiente en inventario.")
                    return

                nuevo_stock = stock_actual - int(cantidad)
                if nuevo_stock > 0:
                    cursor.execute("""
                        UPDATE inventario SET cantStock = %s
                        WHERE idProducto IN (SELECT idProducto FROM productos WHERE codProducto = %s) AND idSucursal = %s
                    """, (nuevo_stock, codigo, self.sucursal_id))
                    QMessageBox.information(self, "Éxito", "Cantidad eliminada exitosamente.")
                else:
                    cursor.execute("""
                        DELETE FROM inventario WHERE idProducto IN (SELECT idProducto FROM productos WHERE codProducto = %s) AND idSucursal = %s
                    """, (codigo, self.sucursal_id))
                    cursor.execute("DELETE FROM productos WHERE codProducto = %s", (codigo,))
                    QMessageBox.information(self, "Éxito", "Producto eliminado completamente.")

            conn.commit()
            cursor.close()
            conn.close()

            # Refrescar el formulario
            self.eliminar_producto()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def ver_inventario_cocina(self):
    # Limpiar el área principal
        for i in reversed(range(self.area_principal_layout.count())):
            widget = self.area_principal_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

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
                mensaje = QLabel("No hay productos en el inventario de cocina para esta sucursal.")
                mensaje.setAlignment(Qt.AlignCenter)
                mensaje.setStyleSheet("font-size: 16px; color: #a67c52; font-weight: bold;")
                self.area_principal_layout.addWidget(mensaje)
                return

            # Crear tabla para mostrar el inventario
            inventario_table = QTableWidget()
            inventario_table.setColumnCount(5)
            inventario_table.setHorizontalHeaderLabels(["Código", "Nombre", "Valor", "Cantidad", "Categoría"])
            inventario_table.setRowCount(len(productos))

            for row, (codigo, nombre, valor, cantidad, categoria) in enumerate(productos):
                inventario_table.setItem(row, 0, QTableWidgetItem(codigo))
                inventario_table.setItem(row, 1, QTableWidgetItem(nombre))
                inventario_table.setItem(row, 2, QTableWidgetItem(f"${valor}"))
                inventario_table.setItem(row, 3, QTableWidgetItem(str(cantidad)))
                inventario_table.setItem(row, 4, QTableWidgetItem(categoria or "Sin categoría"))

            self.area_principal_layout.addWidget(inventario_table)

            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo conectar a la base de datos: {str(e)}")



    def agregar_producto_cocina(self):
        # Limpiar el área principal antes de mostrar el formulario
        for i in reversed(range(self.area_principal_layout.count())):
            widget = self.area_principal_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Crear el formulario
        form_layout = QFormLayout()

        self.tipo_producto_cocina = QComboBox()
        self.tipo_producto_cocina.addItem("Nuevo Producto")
        self.tipo_producto_cocina.addItem("Producto Existente")

        # Campos de entrada
        self.codigo_producto_input_cocina = QLineEdit()
        self.nombre_producto_input_cocina = QLineEdit()  # Solo para nuevos productos
        self.valor_producto_input_cocina = QLineEdit()   # Solo para nuevos productos
        self.cantidad_producto_input_cocina = QLineEdit()

        # Combobox para seleccionar la categoría
        self.categoria_combo_cocina = QComboBox()
        self.cargar_categorias_cocina()

        form_layout.addRow("Tipo de Producto:", self.tipo_producto_cocina)
        form_layout.addRow("Código del Producto:", self.codigo_producto_input_cocina)
        form_layout.addRow("Nombre del Producto:", self.nombre_producto_input_cocina)
        form_layout.addRow("Valor del Producto:", self.valor_producto_input_cocina)
        form_layout.addRow("Cantidad del Producto:", self.cantidad_producto_input_cocina)
        form_layout.addRow("Categoría:", self.categoria_combo_cocina)

        self.tipo_producto_cocina.currentIndexChanged.connect(self.toggle_producto_fields_cocina)

        # Botón para guardar el producto
        btn_guardar = QPushButton("Guardar")
        btn_guardar.clicked.connect(self.guardar_producto_cocina)
        form_layout.addRow(btn_guardar)

        # Mostrar el formulario en el área principal
        widget_formulario = QWidget()
        widget_formulario.setLayout(form_layout)
        self.area_principal_layout.addWidget(widget_formulario)

        # Configurar campos según el tipo de producto
        self.toggle_producto_fields_cocina()

    def toggle_producto_fields_cocina(self):
        if self.tipo_producto_cocina.currentText() == "Nuevo Producto":
            self.nombre_producto_input_cocina.show()
            self.valor_producto_input_cocina.show()
            self.categoria_combo_cocina.show()
        else:
            self.nombre_producto_input_cocina.hide()
            self.valor_producto_input_cocina.hide()
            self.categoria_combo_cocina.hide()

    def guardar_producto_cocina(self):
        codigo = self.codigo_producto_input_cocina.text()
        nombre = self.nombre_producto_input_cocina.text()
        valor = self.valor_producto_input_cocina.text()
        cantidad = self.cantidad_producto_input_cocina.text()

        if not codigo or (self.tipo_producto_cocina.currentText() == "Nuevo Producto" and (not nombre or not valor)) or not cantidad:
            QMessageBox.warning(self, "Error", "Por favor complete todos los campos")
            return

        try:
            conn = obtener_conexion()
            cursor = conn.cursor()

            if self.tipo_producto_cocina.currentText() == "Nuevo Producto":
                cursor.execute(
                    "INSERT INTO productos (codProducto, nProducto, valor, idCategoria) VALUES (%s, %s, %s, %s)",
                    (codigo, nombre, valor, self.categoria_combo_cocina.currentData())
                )
                conn.commit()
                cursor.execute("SELECT idProducto FROM productos WHERE codProducto = %s", (codigo,))
                id_producto = cursor.fetchone()[0]
                cursor.execute(
                    "INSERT INTO casino (idSucursal, idProducto, cantStock) VALUES (%s, %s, %s)",
                    (self.sucursal_id, id_producto, cantidad)
                )
                QMessageBox.information(self, "Éxito", "Producto agregado exitosamente al inventario de cocina.")

            elif self.tipo_producto_cocina.currentText() == "Producto Existente":
                cursor.execute("SELECT idProducto FROM productos WHERE codProducto = %s", (codigo,))
                producto = cursor.fetchone()
                if producto:
                    id_producto = producto[0]
                    cursor.execute(
                        "UPDATE casino SET cantStock = cantStock + %s WHERE idProducto = %s AND idSucursal = %s",
                        (cantidad, id_producto, self.sucursal_id)
                    )
                    QMessageBox.information(self, "Éxito", "Cantidad actualizada exitosamente.")
                else:
                    QMessageBox.warning(self, "Error", "Producto no encontrado.")

            conn.commit()
            cursor.close()
            conn.close()

            # Refrescar el formulario
            self.agregar_producto_cocina()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

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
    # Limpiar el área principal
        for i in reversed(range(self.area_principal_layout.count())):
            widget = self.area_principal_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Crear el formulario
        form_layout = QFormLayout()

        self.codigo_producto_eliminar_input = QLineEdit()
        self.cantidad_producto_eliminar_input = QLineEdit()
        self.eliminar_todo_checkbox_cocina = QCheckBox("Eliminar todo el producto")

        form_layout.addRow("Código del Producto:", self.codigo_producto_eliminar_input)
        form_layout.addRow("Cantidad a eliminar:", self.cantidad_producto_eliminar_input)
        form_layout.addRow(self.eliminar_todo_checkbox_cocina)

        # Botón para eliminar
        btn_eliminar = QPushButton("Eliminar")
        btn_eliminar.clicked.connect(self.confirmar_eliminar_producto_cocina)
        btn_eliminar.setStyleSheet("""
            QPushButton {
                background-color: #a67c52;
                color: white;
                border-radius: 10px;
                padding: 10px 20px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #8b5e3c;
            }
        """)

        # Mostrar el formulario en el área principal
        form_widget = QWidget()
        form_widget.setLayout(form_layout)
        self.area_principal_layout.addWidget(form_widget)
        self.area_principal_layout.addWidget(btn_eliminar)


    def confirmar_eliminar_producto_cocina(self):
        codigo = self.codigo_producto_eliminar_input.text()
        cantidad = self.cantidad_producto_eliminar_input.text()

        if not codigo or (not cantidad and not self.eliminar_todo_checkbox_cocina.isChecked()):
            QMessageBox.warning(self, "Error", "Por favor complete los campos necesarios.")
            return

        try:
            conn = obtener_conexion()
            cursor = conn.cursor()

            if self.eliminar_todo_checkbox_cocina.isChecked():
                cursor.execute("""
                    DELETE FROM casino WHERE idProducto IN (SELECT idProducto FROM productos WHERE codProducto = %s) AND idSucursal = %s
                """, (codigo, self.sucursal_id))
                cursor.execute("DELETE FROM productos WHERE codProducto = %s", (codigo,))
                conn.commit()
                QMessageBox.information(self, "Éxito", "Producto eliminado completamente.")
            else:
                cursor.execute("""
                    SELECT cantStock FROM casino
                    WHERE idProducto IN (SELECT idProducto FROM productos WHERE codProducto = %s) AND idSucursal = %s
                """, (codigo, self.sucursal_id))
                resultado = cursor.fetchone()

                if not resultado:
                    QMessageBox.warning(self, "Error", "Producto no encontrado.")
                    return

                stock_actual = resultado[0]
                if stock_actual < int(cantidad):
                    QMessageBox.warning(self, "Error", "Cantidad insuficiente en inventario.")
                    return

                nuevo_stock = stock_actual - int(cantidad)
                if nuevo_stock > 0:
                    cursor.execute("""
                        UPDATE casino SET cantStock = %s
                        WHERE idProducto IN (SELECT idProducto FROM productos WHERE codProducto = %s) AND idSucursal = %s
                    """, (nuevo_stock, codigo, self.sucursal_id))
                    QMessageBox.information(self, "Éxito", "Cantidad eliminada exitosamente.")
                else:
                    cursor.execute("""
                        DELETE FROM casino WHERE idProducto IN (SELECT idProducto FROM productos WHERE codProducto = %s) AND idSucursal = %s
                    """, (codigo, self.sucursal_id))
                    cursor.execute("DELETE FROM productos WHERE codProducto = %s", (codigo,))
                    QMessageBox.information(self, "Éxito", "Producto eliminado completamente.")

            conn.commit()
            cursor.close()
            conn.close()

            # Refrescar el formulario
            self.eliminar_producto_cocina()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
    
    def traspasar_producto_cocina(self):
    # Limpiar el área principal
        for i in reversed(range(self.area_principal_layout.count())):
            widget = self.area_principal_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Crear el formulario
        form_layout = QFormLayout()

        # Seleccionar sucursal de origen
        self.sucursal_origen_combo = QComboBox()
        self.cargar_sucursales_asociadas()
        form_layout.addRow("Sucursal de Origen:", self.sucursal_origen_combo)

        # Seleccionar producto en inventario de la sucursal de origen
        self.producto_origen_combo = QComboBox()
        self.sucursal_origen_combo.currentIndexChanged.connect(self.cargar_productos_origen)
        form_layout.addRow("Producto a Traspasar:", self.producto_origen_combo)

        # Seleccionar sucursal de destino
        self.sucursal_destino_combo = QComboBox()
        self.cargar_sucursales_destino()
        form_layout.addRow("Sucursal de Destino:", self.sucursal_destino_combo)

        # Campo para cantidad a traspasar
        self.cantidad_traspaso_input = QLineEdit()
        form_layout.addRow("Cantidad a Traspasar:", self.cantidad_traspaso_input)

        # Botón para traspasar
        btn_traspasar = QPushButton("Traspasar")
        btn_traspasar.clicked.connect(self.confirmar_traspaso)
        btn_traspasar.setStyleSheet("""
            QPushButton {
                background-color: #a67c52;
                color: white;
                border-radius: 10px;
                padding: 10px 20px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #8b5e3c;
            }
        """)

        # Mostrar el formulario en el área principal
        form_widget = QWidget()
        form_widget.setLayout(form_layout)
        self.area_principal_layout.addWidget(form_widget)
        self.area_principal_layout.addWidget(btn_traspasar)



    def cargar_sucursales_destino(self):
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

            self.sucursal_destino_combo.clear()
            for sucursal in sucursales:
                self.sucursal_destino_combo.addItem(sucursal[1], sucursal[0])
                
            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar las sucursales: {str(e)}")

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
    # Obtener el idSucursal seleccionado
        sucursal_id = self.sucursal_origen_combo.currentData()
        if not sucursal_id:
            return

        try:
            conn = obtener_conexion()
            cursor = conn.cursor()

            # Seleccionar los productos asociados a la sucursal de origen
            cursor.execute("""
                SELECT p.idProducto, p.nProducto 
                FROM productos p
                JOIN casino c ON p.idProducto = c.idProducto
                WHERE c.idSucursal = %s
            """, (sucursal_id,))
            productos = cursor.fetchall()

            # Limpiar y cargar los productos en el ComboBox
            self.producto_origen_combo.clear()
            if productos:
                for producto in productos:
                    self.producto_origen_combo.addItem(producto[1], producto[0])
            else:
                self.producto_origen_combo.addItem("No hay productos disponibles", None)

            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar los productos: {str(e)}")
            
    def confirmar_traspaso(self):
        sucursal_origen_id = self.sucursal_origen_combo.currentData()
        sucursal_destino_id = self.sucursal_destino_combo.currentData()
        producto_id = self.producto_origen_combo.currentData()
        cantidad = self.cantidad_traspaso_input.text()

        # Validaciones
        if not sucursal_origen_id or not sucursal_destino_id or not producto_id:
            QMessageBox.warning(self, "Error", "Por favor selecciona todas las opciones requeridas.")
            return

        if sucursal_origen_id == sucursal_destino_id:
            QMessageBox.warning(self, "Error", "La sucursal de origen y destino no pueden ser la misma.")
            return

        if not cantidad.isdigit() or int(cantidad) <= 0:
            QMessageBox.warning(self, "Error", "La cantidad debe ser un número positivo.")
            return

        try:
            cantidad = int(cantidad)
            conn = obtener_conexion()
            cursor = conn.cursor()

            # Verificar el stock actual en la sucursal de origen
            cursor.execute("""
                SELECT cantStock 
                FROM casino 
                WHERE idSucursal = %s AND idProducto = %s
            """, (sucursal_origen_id, producto_id))
            resultado = cursor.fetchone()

            if not resultado:
                QMessageBox.warning(self, "Error", "El producto no existe en la sucursal de origen.")
                return

            stock_actual = resultado[0]
            if stock_actual < cantidad:
                QMessageBox.warning(self, "Error", f"No hay suficiente stock en la sucursal de origen. Stock actual: {stock_actual}.")
                return

            # Reducir la cantidad en la sucursal de origen
            cursor.execute("""
                UPDATE casino
                SET cantStock = cantStock - %s
                WHERE idSucursal = %s AND idProducto = %s
            """, (cantidad, sucursal_origen_id, producto_id))

            # Aumentar la cantidad en la sucursal destino
            cursor.execute("""
                INSERT INTO casino (idSucursal, idProducto, cantStock)
                VALUES (%s, %s, %s)
                ON CONFLICT (idSucursal, idProducto)
                DO UPDATE SET cantStock = casino.cantStock + EXCLUDED.cantStock
            """, (sucursal_destino_id, producto_id, cantidad))

            conn.commit()
            cursor.close()
            conn.close()

            # Mensaje de éxito y refrescar
            QMessageBox.information(self, "Éxito", "Producto traspasado exitosamente.")
            self.cargar_productos_origen()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Fallo durante el traspaso: {str(e)}")

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


    def mostrar_calendario(self):
    # Limpia el área principal antes de mostrar el calendario
        self.limpiar_area_principal()

        # Crear un calendario
        self.calendario = QCalendarWidget()
        self.calendario.setGridVisible(True)
        self.calendario.setStyleSheet("""
            /* Fondo general del calendario */
            QCalendarWidget {
                font-size: 16px;
                color: #000000;
                background-color: rgba(245, 245, 245, 0.9); /* Fondo gris claro translúcido */
                border: 1px solid #b28a68; /* Borde café intermedio */
                border-radius: 10px;
            }

            /* Fondo de los días */
            QCalendarWidget QAbstractItemView {
                background-color: rgba(255, 255, 255, 1); /* Fondo blanco */
                color: #000000; /* Texto negro */
                selection-background-color: #a67c52; /* Fondo café oscuro para selección */
                selection-color: white; /* Texto blanco para selección */
            }

            /* Botones de navegación */
            QCalendarWidget QToolButton {
                background-color: #a67c52; /* Fondo café oscuro */
                color: white; /* Texto blanco */
                border: none;
                font-size: 16px;
                font-weight: bold;
                padding: 5px;
                border-radius: 5px;
            }
            QCalendarWidget QToolButton:hover {
                background-color: #8b5e3c; /* Fondo café más oscuro */
            }
            QCalendarWidget QToolButton:pressed {
                background-color: #6d4229; /* Fondo café intenso */
            }

            /* Encabezados de días */
            QCalendarWidget QHeaderView::section {
                background-color: #a67c52; /* Fondo café oscuro */
                color: white; /* Texto blanco */
                font-size: 14px;
                font-weight: bold;
                border: 1px solid #8b5e3c; /* Borde café más oscuro */
                padding: 5px;
            }

            /* SpinBox del año */
            QCalendarWidget QSpinBox {
                margin: 2px;
                border: 1px solid #a67c52; /* Borde café oscuro */
                background-color: #ffffff; /* Fondo blanco */
                color: #000000; /* Texto negro */
                font-size: 14px;
                border-radius: 5px;
                padding: 2px;
            }
            QCalendarWidget QSpinBox::up-button {
                subcontrol-origin: border;
                subcontrol-position: top right;
                width: 16px;
            }
            QCalendarWidget QSpinBox::down-button {
                subcontrol-origin: border;
                subcontrol-position: bottom right;
                width: 16px;
            }
        """)

        # Campo para ingresar la descripción del evento
        self.evento_input = QLineEdit()
        self.evento_input.setPlaceholderText("Descripción del evento")
        self.evento_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #b28a68;
                border-radius: 10px;
                padding: 8px;
                font-size: 14px;
            }
        """)

        # Botón para guardar un evento
        btn_guardar_evento = QPushButton("Guardar Evento")
        btn_guardar_evento.setFixedHeight(40)
        btn_guardar_evento.setStyleSheet("""
            QPushButton {
                background-color: #a67c52;
                color: white;
                border-radius: 10px;
                padding: 10px 20px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #8b5e3c;
            }
        """)
        btn_guardar_evento.clicked.connect(self.guardar_evento)

        # Conectar la selección de fecha al evento para mostrar los eventos del día
        self.calendario.selectionChanged.connect(self.mostrar_eventos_del_dia)

        # Layout para el calendario y el formulario
        layout = QVBoxLayout()
        layout.addWidget(self.calendario)
        layout.addWidget(QLabel("Descripción del evento:"))
        layout.addWidget(self.evento_input)
        layout.addWidget(btn_guardar_evento)

        # Mostrar el contenido en el área principal
        widget = QWidget()
        widget.setLayout(layout)
        self.area_principal_layout.addWidget(widget)

    def guardar_evento(self):
        fecha_seleccionada = self.calendario.selectedDate().toString("yyyy-MM-dd")
        descripcion = self.evento_input.text().strip()

        if not descripcion:
            QMessageBox.warning(self, "Error", "La descripción del evento no puede estar vacía.")
            return

        try:
            conn = obtener_conexion()
            cursor = conn.cursor()

            # Insertar el evento en la tabla calendario
            cursor.execute("""
                INSERT INTO calendario (fecha, evento, idsucursal)
                VALUES (%s, %s, %s)
            """, (fecha_seleccionada, descripcion, self.sucursal_id))

            conn.commit()
            cursor.close()
            conn.close()

            QMessageBox.information(self, "Éxito", f"Evento guardado para {fecha_seleccionada}: {descripcion}")
            self.evento_input.clear()  # Limpiar el campo de texto después de guardar
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo guardar el evento: {str(e)}")

    def mostrar_eventos_del_dia(self):
        fecha = self.calendario.selectedDate()
        eventos = self.cargar_eventos_calendario(fecha)

        if eventos:
            eventos_str = "\n".join(f"- {evento}" for evento in eventos)
            QMessageBox.information(self, "Eventos", f"Eventos para {fecha.toString('yyyy-MM-dd')}:\n{eventos_str}")
        else:
            QMessageBox.information(self, "Eventos", f"No hay eventos para {fecha.toString('yyyy-MM-dd')}")

    def cargar_eventos_calendario(self, fecha):
        """
        Carga los eventos de una fecha específica desde la base de datos.
        """
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()

            # Convertir la fecha al formato adecuado
            fecha_str = fecha.toString("yyyy-MM-dd")

            cursor.execute("""
                SELECT evento FROM calendario
                WHERE fecha = %s AND idsucursal = %s
            """, (fecha_str, self.sucursal_id))
            eventos = cursor.fetchall()

            cursor.close()
            conn.close()

            return [evento[0] for evento in eventos]
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar los eventos: {str(e)}")
            return []


    def ver_estadisticas(self):
    # Limpia el área principal antes de mostrar las estadísticas
        self.limpiar_area_principal()

        # Título de la sección
        titulo_label = QLabel("Estadísticas del Sistema")
        titulo_label.setAlignment(Qt.AlignCenter)
        titulo_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #6d4229;
        """)

        # Dropdown para seleccionar el tipo de gráfico
        tipo_grafico_combo = QComboBox()
        tipo_grafico_combo.addItems(["Ventas Totales por Mes", "Productos Más Vendidos", "Métodos de Pago"])
        tipo_grafico_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                font-size: 14px;
                border-radius: 10px;
                border: 1px solid #b28a68;
                background-color: rgba(255, 255, 255, 0.9);
            }
        """)

        # Canvas para los gráficos
        self.grafico_canvas = FigureCanvas(Figure(figsize=(5, 4)))
        self.grafico_axes = self.grafico_canvas.figure.add_subplot(111)

        # Botón para generar el gráfico
        btn_generar = QPushButton("Generar Gráfico")
        btn_generar.setFixedHeight(40)
        btn_generar.setStyleSheet("""
            QPushButton {
                background-color: #a67c52;
                color: white;
                border-radius: 10px;
                padding: 10px 20px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #8b5e3c;
            }
        """)

        # Conectar el botón al evento de generación del gráfico
        btn_generar.clicked.connect(lambda: self.generar_grafico_dinamico(tipo_grafico_combo.currentText()))

        # Layout para la sección de estadísticas
        layout = QVBoxLayout()
        layout.addWidget(titulo_label)
        layout.addWidget(tipo_grafico_combo)
        layout.addWidget(self.grafico_canvas)
        layout.addWidget(btn_generar)

        # Mostrar el contenido en el área principal
        widget = QWidget()
        widget.setLayout(layout)
        self.area_principal_layout.addWidget(widget)



    def generar_grafico_dinamico(self, tipo_grafico):
    # Limpia los ejes del gráfico
        self.grafico_axes.clear()

        try:
            conn = obtener_conexion()
            cursor = conn.cursor()

            if tipo_grafico == "Ventas Totales por Mes":
                cursor.execute("""
                    SELECT DATE_TRUNC('month', v.fecha) AS mes, SUM(v.totalVenta) AS total
                    FROM Ventas v
                    WHERE v.idSucursal = %s
                    GROUP BY mes
                    ORDER BY mes;
                """, (self.sucursal_id,))
                datos = cursor.fetchall()
                meses = [fila[0].strftime("%b %Y") for fila in datos]
                totales = [fila[1] for fila in datos]
                self.grafico_axes.bar(meses, totales, color="#a67c52")
                self.grafico_axes.set_title("Ventas Totales por Mes")
                self.grafico_axes.set_ylabel("Total Ventas ($)")
                self.grafico_axes.set_xlabel("Meses")

            elif tipo_grafico == "Productos Más Vendidos":
                cursor.execute("""
                    SELECT p.nProducto, SUM(vd.cantidad_vendida) AS total_vendido
                    FROM VentaDetalle vd
                    JOIN Productos p ON vd.idProducto = p.idProducto
                    JOIN Ventas v ON vd.idVentas = v.idVentas
                    WHERE v.idSucursal = %s
                    AND v.fecha >= CURRENT_DATE - INTERVAL '1 month'
                    GROUP BY p.nProducto
                    ORDER BY total_vendido DESC
                    LIMIT 5;
                """, (self.sucursal_id,))
                datos = cursor.fetchall()
                productos = [fila[0] for fila in datos]
                cantidades = [fila[1] for fila in datos]
                self.grafico_axes.barh(productos, cantidades, color="#8b5e3c")
                self.grafico_axes.set_title("Productos Más Vendidos")
                self.grafico_axes.set_xlabel("Cantidad Vendida")

            elif tipo_grafico == "Métodos de Pago":
                cursor.execute("""
                    SELECT mp.nMetodo, COUNT(v.idVentas) AS cantidad
                    FROM Ventas v
                    JOIN MetodoPago mp ON v.idMetodo = mp.idMetodo
                    WHERE v.idSucursal = %s
                    GROUP BY mp.nMetodo
                    ORDER BY cantidad DESC;
                """, (self.sucursal_id,))
                datos = cursor.fetchall()
                metodos = [fila[0] for fila in datos]
                cantidades = [fila[1] for fila in datos]
                self.grafico_axes.pie(cantidades, labels=metodos, autopct="%1.1f%%", startangle=90, colors=["#a67c52", "#8b5e3c", "#6d4229"])
                self.grafico_axes.set_title("Distribución por Método de Pago")

            # Actualiza el canvas con el nuevo gráfico
            self.grafico_canvas.draw()
            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar los datos: {str(e)}")



