# ventanas/caja.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QLabel, QPushButton, QTableWidget, QTableWidgetItem
from db import obtener_conexion

class VentanaCaja(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Caja - Realizar Venta")
        self.setGeometry(100, 100, 500, 400)

        # Layout principal
        layout = QVBoxLayout()

        # Barra de Búsqueda
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Buscar producto por nombre o código")
        self.search_bar.returnPressed.connect(self.buscar_producto)  # Conectar al método de búsqueda
        layout.addWidget(self.search_bar)

        # Tabla de Carrito de Compras
        self.carrito_table = QTableWidget(self)
        self.carrito_table.setColumnCount(3)
        self.carrito_table.setHorizontalHeaderLabels(["Producto", "Cantidad", "Subtotal"])
        layout.addWidget(self.carrito_table)

        # Total de la Compra
        self.total_label = QLabel("Total: $0.00", self)
        layout.addWidget(self.total_label)

        # Botón para Finalizar Compra
        self.btn_finalizar = QPushButton("Finalizar Compra", self)
        layout.addWidget(self.btn_finalizar)

        self.setLayout(layout)

        # Conectar el botón a la función de finalizar compra
        self.btn_finalizar.clicked.connect(self.finalizar_compra)

    def buscar_producto(self):
        producto_nombre = self.search_bar.text()
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT Nombre_Producto, Valor_Producto FROM Producto WHERE Nombre_Producto ILIKE %s", (f"%{producto_nombre}%",))
        productos = cursor.fetchall()

        # Limpiar tabla antes de mostrar nuevos resultados
        self.carrito_table.setRowCount(0)
        
        for row_index, (nombre, valor) in enumerate(productos):
            self.carrito_table.insertRow(row_index)
            self.carrito_table.setItem(row_index, 0, QTableWidgetItem(nombre))
            self.carrito_table.setItem(row_index, 1, QTableWidgetItem("1"))  # Cantidad por defecto 1
            self.carrito_table.setItem(row_index, 2, QTableWidgetItem(f"${valor}"))

        cursor.close()
        conn.close()

    def finalizar_compra(self):
        # Lógica para finalizar la compra y descontar inventario
        print("Compra finalizada")
