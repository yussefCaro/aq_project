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
from django.template.loader import get_template
import pdfkit


def solicitud(request):
    if request.method == "POST":
        nit = request.POST.get('nit')  # Obtener el NIT ingresado
        cliente = Cliente.objects.filter(nit=nit).first()

        if cliente:
            # Si el cliente existe, redirigir a la vista de detalles
            return redirect('ver_cliente', cliente_id=cliente.id)
        else:
            # Si el cliente no existe, redirigir a la vista de creación
            return redirect('crear_cliente', nit=nit)  # Redirige a crear nuevo cliente

    # Mostrar el formulario vacío solo con el campo NIT
    return render(request, 'solicitudes/solicitud_form.html')



def ver_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)

    # Si se quiere permitir la edición, puedes agregar un formulario aquí.
    # Por ahora solo mostrar los datos:

    return render(request, 'solicitudes/ver_cliente.html', {'cliente': cliente})

def crear_cliente(request, nit):
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            nuevo_cliente = form.save()
            return redirect('ver_cliente', cliente_id=nuevo_cliente.id)
    else:
        form = ClienteForm(initial={'nit': nit})  # Prellenar con el NIT ingresado

    return render(request, 'solicitudes/crear_cliente.html', {'form': form})


def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)

    if request.method == "POST":
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('ver_cliente', cliente_id=cliente.id)
    else:
        form = ClienteForm(instance=cliente)

    return render(request, 'solicitudes/editar_cliente.html', {'form': form, 'cliente': cliente})





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