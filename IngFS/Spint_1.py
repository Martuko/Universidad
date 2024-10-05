import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit, QLabel, QPushButton, 
    QTableWidget, QTableWidgetItem, QComboBox, QHBoxLayout
)

class VentanaPrincipal(QWidget):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana
        self.setWindowTitle('Sistema de Ventas - Casino')
        self.setGeometry(100, 100, 600, 400)
        
        # Layout principal
        layout = QVBoxLayout()

        # Barra de búsqueda
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Buscar producto por nombre o código")
        layout.addWidget(self.search_bar)

        # Tabla de productos seleccionados
        self.table = QTableWidget(self)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Producto", "Cantidad", "Subtotal"])
        layout.addWidget(self.table)

        # Mostrar el total de la compra
        self.total_label = QLabel("Total: $0.00", self)
        layout.addWidget(self.total_label)

        # Selección de método de pago
        hbox_metodo_pago = QHBoxLayout()
        self.metodo_pago_label = QLabel("Método de Pago:", self)
        self.metodo_pago_combo = QComboBox(self)
        self.metodo_pago_combo.addItems(["Crédito", "Débito", "Efectivo", "JUNAEB", "Amipass"])
        hbox_metodo_pago.addWidget(self.metodo_pago_label)
        hbox_metodo_pago.addWidget(self.metodo_pago_combo)
        layout.addLayout(hbox_metodo_pago)

        # Botón para generar la boleta
        self.generar_boleta_btn = QPushButton("Generar Boleta", self)
        layout.addWidget(self.generar_boleta_btn)

        # Configurar el layout principal
        self.setLayout(layout)

        # Conectar la barra de búsqueda con la función de búsqueda (sin funcionalidad aún)
        self.search_bar.textChanged.connect(self.buscar_producto)

    def buscar_producto(self):
        # Esta función se ejecuta cuando se escribe en la barra de búsqueda
        # Aquí podrías agregar la lógica de búsqueda de productos
        input_text = self.search_bar.text()
        print(f"Buscando producto: {input_text}")

# Inicialización de la aplicación
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec_())
