from django.shortcuts import redirect, get_object_or_404, render
from django.http import HttpResponse
from django.urls import reverse
from .models import Cliente
from .forms import ClienteForm, SolicitudForm
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Vista para manejar el formulario de solicitud
def solicitud(request):
    if request.method == "POST":
        nit = request.POST.get('nit')
        cliente = Cliente.objects.filter(nit=nit).first()

        if cliente:
            return redirect('ver_cliente', cliente_id=cliente.id)
        else:
            return redirect('crear_cliente', nit=nit)

    return render(request, 'solicitudes/solicitud_form.html')


# Vista para enviar la solicitud con fecha
def enviar_solicitud(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)

    if request.method == "POST":
        form = SolicitudForm(request.POST)
        if form.is_valid():
            cliente.fecha_solicitud = form.cleaned_data['fecha_solicitud']
            cliente.save()
            return redirect('ver_cliente', cliente_id=cliente.id)
    else:
        form = SolicitudForm(initial={'fecha_solicitud': date.today()})

    return render(request, 'solicitudes/enviar_solicitud.html', {'form': form, 'cliente': cliente})


# Vista para ver los datos del cliente
def ver_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    return render(request, 'solicitudes/ver_cliente.html', {'cliente': cliente})


# Vista para crear un nuevo cliente con el NIT prellenado
def crear_cliente(request, nit=None):
    # Si se proporciona un nit, intentamos obtener un cliente
    cliente = None
    if nit:
        cliente = Cliente.objects.filter(nit=nit).first()

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            cliente = form.save()  # Guarda el cliente
            return redirect('ver_cliente', cliente_id=cliente.id)  # Redirige a la vista de ver_cliente
    else:
        form = ClienteForm(instance=cliente)

    return render(request, 'solicitudes/crear_cliente.html', {'form': form, 'cliente': cliente})


# Vista para editar datos del cliente
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


# Generación de PDF con datos del cliente
def generar_solicitud_pdf(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="solicitud_servicio.pdf"'

    pdf = canvas.Canvas(response, pagesize=letter)
    pdf.setFont("Helvetica", 10)

    # Título
    pdf.drawString(100, 750, "Solicitud de Auditoría")

    # Datos del cliente
    pdf.drawString(100, 730, f"NIT: {cliente.nit}")
    pdf.drawString(100, 710, f"Nombre del Propietario: {cliente.nombre_propietario}")
    pdf.drawString(100, 690, f"Establecimiento Comercial: {cliente.nombre_establecimiento}")
    pdf.drawString(100, 670, f"Representante Legal: {cliente.representante_legal}")
    pdf.drawString(100, 650, f"Ciudad: {cliente.ciudad}")
    pdf.drawString(100, 630, f"Departamento: {cliente.departamento}")
    pdf.drawString(100, 610, f"Correo Electrónico: {cliente.correo_electronico}")
    pdf.drawString(100, 590, f"Teléfono: {cliente.telefono_celular}")

    # Fecha de solicitud
    fecha_solicitud = cliente.fecha_solicitud.strftime("%d/%m/%Y") if cliente.fecha_solicitud else "No registrada"
    pdf.drawString(100, 570, f"Fecha de Solicitud: {fecha_solicitud}")

    # Finalizar PDF
    pdf.showPage()
    pdf.save()

    return response
