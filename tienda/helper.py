from django.conf import settings
from django.core.mail import EmailMultiAlternatives
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import letter
from .models import *

class helper:
    def printPDF(id):
        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
        textob = c.beginText()
        
        # Establece origen y fuente
        textob.setTextOrigin(cm, cm)
        textob.setFont("Helvetica", 14)

        textob.textLine(text="FACTURA")

        # Medir la página y el texto "El Prioste"
        page_width, _ = letter
        text = "EL PRIOSTE"
        text_width = c.stringWidth(text, "Helvetica", 14)

        # Escribir "El Prioste" directamente sobre el canvas (no textob)
        c.drawString(page_width - text_width - cm, cm, text)

        # ----Primeras líneas----
        compra = Compra.objects.get(pk=id)
        primeras_lineas = [
            "",
            f"Fecha de factura: {compra.fecha.date()}",
            f"Número de factura: {compra.id}",
            "",
            compra.nombre_completo,
        ]
        
        # ----Pintar esas líneas en el objeto----
        for linea in primeras_lineas:
            textob.textLine(linea)

        # Avance de cursor: meter una linea en blanco para mover Dirección hacia abajo de la raya
        textob.textLine("")

        y_header = textob.getY()
        c.setFont("Helvetica-Bold", 14)
        c.drawString(cm,                    y_header, "Descripción")
        c.drawString(cm + 200,              y_header, "Unidades")
        c.drawString(cm + 330,              y_header, "Precio Unitario")
        c.drawString(page_width - cm - 80,  y_header, "Precio")

        c.line(cm, y_header + 15, page_width - cm, y_header + 15)

        textob.moveCursor(0, 30)
        c.setFont("Helvetica", 12)
        y_producto = y_header + 30

        for item in compra.productocompra_set.all():
            producto_nombre = item.producto.nombre
            unidades = item.cantidad
            precio_unitario = item.producto.precio
            precio_linea = unidades * precio_unitario

            # ----Pintar cada columna con las mismas X que en el encabezado
            c.drawString(cm,                    y_producto, producto_nombre)
            c.drawString(cm + 200,              y_producto, str(unidades))
            c.drawString(cm + 330,              y_producto, f"{precio_unitario:.2f}€")
            c.drawString(page_width - cm - 80,  y_producto, f"{precio_linea:.2f}€")

            y_producto += 20
        
        y_producto += 20
        
        c.setFont("Helvetica-Bold", 14)
        c.drawString(cm, y_producto, "DATOS DE LA ENTREGA")

        c.setFont("Helvetica", 12)
        c.line(cm, y_producto + 15, page_width - cm, y_producto + 15)

        y_producto += 30

        segundas_lineas = [
            f"Dirección: {compra.direccion}",
            f"Dni: {compra.dni}",
            f"Código postal y ciudad: {compra.cod_postal}, {compra.ciudad}",
            f"Email: {compra.email}",
            "",
        ]

        for line in segundas_lineas:
            c.drawString(cm,        y_producto, line)
            y_producto+=20

        y_producto+=40

        c.setFont("Helvetica-Bold", 16)
        total = f"TOTAL: {compra.totalCompra}"
        total_width = c.stringWidth(total, "Helvetica", 16)
        c.drawString(page_width - total_width - cm, y_producto, total)

        # Para terminar
        c.drawText(textob)
        c.showPage()
        c.save()
        buf.seek(0)

        return buf

    def enviar_mail(compra):
        subject = f"Factura {compra.nombre_completo}"

        message = EmailMultiAlternatives(
            subject,
            f"Factura número {compra.id}",
            settings.EMAIL_HOST_USER,
            [compra.email]
        )

        buf = helper.printPDF(compra.id)

        message.attach(
            "pdf_factura",
            buf.read(),
            "application/pdf"
        )

        message.send()