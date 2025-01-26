from django.shortcuts import  redirect, get_object_or_404
from django.http import HttpResponse
from .models import Cliente
from .forms import ClienteForm
from django.shortcuts import render
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .forms import SolicitudForm
from django.urls import reverse
import datetime


def solicitud(request):
    if request.method == "POST":
        nit = request.POST.get('nit')
        cliente = Cliente.objects.filter(nit=nit).first()

        if cliente:
            # Si el cliente existe, editar los datos
            if request.POST.get('editar_datos'):
                cliente.nombre_establecimiento = request.POST.get('nombre_establecimiento')
                cliente.telefono_celular = request.POST.get('telefono_celular')
                cliente.save()

            # Redirigir a la vista del PDF con el ID del cliente
            return redirect('generar_solicitud_pdf', cliente_id=cliente.id)

        else:
            # Si el cliente no existe, crear uno nuevo
            form = ClienteForm(request.POST)
            if form.is_valid():
                nuevo_cliente = form.save()
                # Redirigir a la vista del PDF con el ID del nuevo cliente
                return redirect('generar_solicitud_pdf', cliente_id=nuevo_cliente.id)
            else:
                # Si el formulario no es válido, mostrar el formulario con errores
                return render(request, 'solicitudes/solicitud_form.html', {'form': form})

    else:
        # Si el método no es POST, renderizar el formulario vacío
        form = ClienteForm()
        return render(request, 'solicitudes/solicitud_form.html', {'form': form})





def generar_solicitud_pdf(request, cliente_id):
    # Obtener los datos del cliente por el ID
    cliente = get_object_or_404(Cliente, id=cliente_id)

    # Crear la respuesta PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="solicitud_servicio.pdf"'

    # Crear el objeto canvas para el PDF
    pdf = canvas.Canvas(response, pagesize=letter)

    # Agregar contenido al PDF
    pdf.setFont("Helvetica", 10)
    pdf.drawString(100, 750, f"Solicitud de Auditoría")
    pdf.drawString(100, 730, f"Nit: {cliente.nit}")
    pdf.drawString(100, 710, f"Nombre del Propietario: {cliente.nombre_propietario}")
    pdf.drawString(100, 690, f"Establecimiento Comercial: {cliente.nombre_establecimiento}")
    pdf.drawString(100, 670, f"Representante Legal: {cliente.representante_legal}")
    pdf.drawString(100, 650, f"Ciudad: {cliente.ciudad}")
    pdf.drawString(100, 630, f"Departamento: {cliente.departamento}")
    pdf.drawString(100, 610, f"Correo Electrónico: {cliente.correo_electronico}")
    pdf.drawString(100, 590, f"Teléfono: {cliente.telefono_celular}")

    # Finalizar el PDF
    pdf.showPage()
    pdf.save()

    return response

