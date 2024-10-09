# ventanas/administrador.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton

class VentanaAdministrador(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Administrador - Gestión de Inventario")
        self.setGeometry(100, 100, 600, 500)
        
        # Layout principal
        layout = QVBoxLayout()
        
        # Botón para ver inventario
        self.btn_ver_inventario = QPushButton("Ver Inventario")
        layout.addWidget(self.btn_ver_inventario)
        
        # Botón para agregar producto
        self.btn_agregar_producto = QPushButton("Agregar Producto")
        layout.addWidget(self.btn_agregar_producto)
        
        # Botón para eliminar producto
        self.btn_eliminar_producto = QPushButton("Eliminar Producto")
        layout.addWidget(self.btn_eliminar_producto)
        
        # Botón para ver estadísticas
        self.btn_ver_estadisticas = QPushButton("Ver Estadísticas")
        layout.addWidget(self.btn_ver_estadisticas)
        
        self.setLayout(layout)
        
        # Conectar botones a funciones (placeholders)
        self.btn_ver_inventario.clicked.connect(self.ver_inventario)
        self.btn_agregar_producto.clicked.connect(self.agregar_producto)
        self.btn_eliminar_producto.clicked.connect(self.eliminar_producto)
        self.btn_ver_estadisticas.clicked.connect(self.ver_estadisticas)
    
    def ver_inventario(self):
        print("Inventario mostrado")
        
    def agregar_producto(self):
        print("Producto agregado")
    
    def eliminar_producto(self):
        print("Producto eliminado")
    
    def ver_estadisticas(self):
        print("Estadísticas mostradas")
