# ventanas/caja.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QLabel, QPushButton, QTableWidget, QTableWidgetItem

class VentanaCaja(QWidget):
    def __init__(self, sucursal):
        super().__init__()
        self.sucursal = sucursal  # Almacenar sucursal seleccionada
        self.setWindowTitle("Caja - Realizar Venta")
        self.setGeometry(100, 100, 500, 400)

        # Layout principal
        layout = QVBoxLayout()

        # Barra de Búsqueda
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Buscar producto por nombre o código")
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

    def finalizar_compra(self):
        # Lógica para finalizar la compra y descontar inventario
        print("Compra finalizada en la sucursal:", self.sucursal)
