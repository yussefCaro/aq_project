from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from solicitudes.models import Solicitud
from .models import Programacion
from django.http import HttpResponse
from django.template.loader import get_template
import pdfkit  # Instala con: pip install pdfkit




# Definimos los días de auditoría por nivel
DIAS_AUDITORIA = {
    "Nivel 1": {"etapa_1": 0.5, "etapa_2": 1},
    "Nivel 2": {"etapa_1": 0.5, "etapa_2": 1.5},
    "Nivel 3": {"etapa_1": 0.5, "etapa_2": 2},
    "Nivel 3 con Formación de Instructores": {"etapa_1": 0.5, "etapa_2": 2.5},
}


@login_required
def listado_solicitudes(request):
    """ Muestra la lista de solicitudes pendientes y permite programarlas. """
    solicitudes = Solicitud.objects.filter(estado="Pendiente")  # Solo solicitudes pendientes
    usuarios = User.objects.all()  # Lista de usuarios para asignar auditores

    if request.method == "POST":
        solicitud_id = request.POST.get("solicitud_id")
        fecha_etapa_1 = request.POST.get("fecha_etapa_1")
        hora_etapa_1 = request.POST.get("hora_etapa_1")
        fecha_etapa_2 = request.POST.getlist("fecha_etapa_2[]")  # Lista de fechas
        hora_etapa_2 = request.POST.get("hora_etapa_2")
        auditor_id = request.POST.get("auditor")

        solicitud = get_object_or_404(Solicitud, id=solicitud_id)
        auditor = get_object_or_404(User, id=auditor_id)

        # Obtener el nivel del CEA y definir los días de auditoría
        nivel = solicitud.cliente.nivel_cea  # Asegúrate de que `Solicitud` tiene un campo `nivel_cea`
        dias_etapa_1 = DIAS_AUDITORIA.get(nivel, {}).get("etapa_1", 0.5)
        dias_etapa_2 = DIAS_AUDITORIA.get(nivel, {}).get("etapa_2", 1)

        # Crear o actualizar la programación
        programacion, created = Programacion.objects.get_or_create(solicitud=solicitud)
        programacion.fecha_etapa_1 = fecha_etapa_1
        programacion.hora_etapa_1 = hora_etapa_1
        programacion.dias_auditoria_etapa_1 = dias_etapa_1
        programacion.fecha_etapa_2 = fecha_etapa_2
        programacion.hora_etapa_2 = hora_etapa_2
        programacion.dias_auditoria_etapa_2 = dias_etapa_2
        programacion.auditor = auditor
        programacion.estado = "Programada"
        programacion.save()

        # Cambiar estado de la solicitud a 'Programada'
        solicitud.estado = "Programada"
        solicitud.save()

        return redirect("listado_solicitudes")

    return render(request, "programacion/listado.html", {"solicitudes": solicitudes, "usuarios": usuarios})


@login_required
def cambiar_estado(request, solicitud_id):
    """ Cambia el estado de una solicitud. """
    solicitud = get_object_or_404(Solicitud, id=solicitud_id)

    if request.method == "POST":
        nuevo_estado = request.POST.get("estado")
        if nuevo_estado in ["Pendiente", "Aprobada", "Rechazada", "Programada"]:
            solicitud.estado = nuevo_estado
            solicitud.save()

    return redirect("listado_solicitudes")

@login_required
def listado_programaciones(request):
    """ Muestra la lista de solicitudes programadas. """
    programaciones = Programacion.objects.select_related("solicitud__cliente", "auditor").filter(estado="Programada")

    return render(request, "programacion/listado_programaciones.html", {"programaciones": programaciones})


@login_required
def imprimir_programacion(request, programacion_id):
    programacion = get_object_or_404(Programacion, id=programacion_id)

    template = get_template("programacion/programacion_pdf.html")
    html = template.render({"programacion": programacion})

    # Configurar PDF
    options = {
        "page-size": "Letter",
        "encoding": "UTF-8",
    }

    pdf = pdfkit.from_string(html, False, options=options)

    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="programacion.pdf"'
    return response
