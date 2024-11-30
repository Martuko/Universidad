import os
from fpdf import FPDF
from PyQt5.QtWidgets import QMessageBox
from db import obtener_conexion

class BoletaPDF:
    def __init__(self, id_venta, total):
        self.id_venta = id_venta
        self.total = total

    def generar_boleta(self):
        # Crear una instancia de FPDF
        pdf = FPDF()
        pdf.add_page()

        # Título de la boleta
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, txt="Boleta de Venta", ln=True, align='C')

        # Detalles de la venta
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"ID Venta: {self.id_venta}", ln=True, align='L')

        # Espacio
        pdf.cell(200, 10, txt="", ln=True, align='C')

        # Encabezado de la tabla
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(80, 10, txt="Producto", border=1)
        pdf.cell(40, 10, txt="Cantidad", border=1)
        pdf.cell(40, 10, txt="Subtotal", border=1)
        pdf.ln()  # Nueva línea

        # Conectar a la base de datos para obtener los detalles de la venta
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()

            # Obtener los detalles de la venta desde `detalle_venta`
            cursor.execute("""
                SELECT p.nProducto, dv.cantidad_vendida, dv.subTotal
                FROM ventadetalle dv
                JOIN productos p ON dv.idProducto = p.idProducto
                WHERE dv.idVentas = %s
            """, (self.id_venta,))

            detalles = cursor.fetchall()

            # Llenar la tabla con los productos vendidos
            pdf.set_font("Arial", size=12)
            for detalle in detalles:
                nombre_producto, cantidad, subtotal = detalle
                pdf.cell(80, 10, txt=nombre_producto, border=1)
                pdf.cell(40, 10, txt=str(cantidad), border=1)
                pdf.cell(40, 10, txt=f"$ {subtotal:.2f}", border=1)
                pdf.ln()

            cursor.close()
            conn.close()

            # Total de la venta
            pdf.cell(200, 10, txt="", ln=True, align='C')
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(120, 10, txt="Total", border=1)
            pdf.cell(40, 10, txt=f"$ {self.total:.2f}", border=1)
            pdf.ln()

        except Exception as e:
            print(f"No se pudo generar la boleta: {str(e)}")
            return None

        # Guardar el PDF en el sistema
        output_path = os.path.join(os.path.expanduser("~"), f"boleta_venta_{self.id_venta}.pdf")
        pdf.output(output_path)

        return output_path