from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from cotizaciones.models import Cotizacion  # Se cambia Solicitud por Cotizacion
from .models import Programacion
from django.http import HttpResponse
from django.template.loader import get_template, render_to_string
import pdfkit  # Instala con: pip install pdfkit
from django.conf import settings
import json

# Definimos los días de auditoría por nivel
DIAS_AUDITORIA = {
    "Nivel 1": {"etapa_1": 0.5, "etapa_2": 1},
    "Nivel 2": {"etapa_1": 0.5, "etapa_2": 1.5},
    "Nivel 3": {"etapa_1": 0.5, "etapa_2": 2},
    "Nivel 3 con Formación de Instructores": {"etapa_1": 0.5, "etapa_2": 2.5},
}

@login_required
def listado_cotizaciones(request):
    """ Muestra la lista de cotizaciones pendientes y permite programarlas. """
    cotizaciones = Cotizacion.objects.filter(estado="Pendiente")  # Solo cotizaciones pendientes
    usuarios = User.objects.all()  # Lista de usuarios para asignar auditores

    if request.method == "POST":
        cotizacion_id = request.POST.get("cotizacion_id")
        fecha_etapa_1 = request.POST.get("fecha_etapa_1")
        hora_etapa_1 = request.POST.get("hora_etapa_1")
        fecha_etapa_2 = request.POST.getlist("fecha_etapa_2[]")  # Lista de fechas
        hora_etapa_2 = request.POST.get("hora_etapa_2")
        auditor_id = request.POST.get("auditor")

        cotizacion = get_object_or_404(Cotizacion, id=cotizacion_id)
        auditor = get_object_or_404(User, id=auditor_id)

        # Obtener el nivel del CEA y definir los días de auditoría
        nivel = cotizacion.solicitud.cliente.nivel_cea  # Se usa cotizacion.solicitud.cliente
        dias_etapa_1 = DIAS_AUDITORIA.get(nivel, {}).get("etapa_1", 0.5)
        dias_etapa_2 = DIAS_AUDITORIA.get(nivel, {}).get("etapa_2", 1)

        # Crear o actualizar la programación
        programacion, created = Programacion.objects.get_or_create(cotizacion=cotizacion)
        programacion.fecha_etapa_1 = fecha_etapa_1
        programacion.hora_etapa_1 = hora_etapa_1
        programacion.dias_auditoria_etapa_1 = dias_etapa_1
        programacion.fecha_etapa_2 = fecha_etapa_2
        programacion.hora_etapa_2 = hora_etapa_2
        programacion.dias_auditoria_etapa_2 = dias_etapa_2
        programacion.auditor = auditor
        programacion.estado = "Programada"
        programacion.save()

        # Cambiar estado de la cotización a 'Programada'
        cotizacion.estado = "Programada"
        cotizacion.save()

        return redirect("listado_cotizaciones")

    return render(request, "programacion/listado.html", {"cotizaciones": cotizaciones, "usuarios": usuarios})


@login_required
def cambiar_estado(request, cotizacion_id):
    """ Cambia el estado de una cotización. """
    cotizacion = get_object_or_404(Cotizacion, id=cotizacion_id)

    if request.method == "POST":
        nuevo_estado = request.POST.get("estado")
        if nuevo_estado in ["Pendiente", "Aprobada", "Rechazada", "Programada"]:
            cotizacion.estado = nuevo_estado
            cotizacion.save()

    return redirect("listado_cotizaciones")


@login_required
def listado_programaciones(request):
    """ Muestra la lista de cotizaciones programadas. """
    programaciones = Programacion.objects.select_related("cotizacion__solicitud__cliente", "auditor").filter(estado="Programada")

    return render(request, "programacion/listado_programaciones.html", {"programaciones": programaciones})


@login_required
def imprimir_programacion(request, programacion_id):
    programacion = get_object_or_404(Programacion, id=programacion_id)

    # Convertir la cadena JSON a una lista de fechas
    if isinstance(programacion.fecha_etapa_2, str):
        programacion.fecha_etapa_2 = json.loads(programacion.fecha_etapa_2)

    # Renderizar el HTML desde una plantilla
    html = render_to_string("programacion/imprimir.html", {"programacion": programacion})

    # Configurar opciones de pdfkit
    options = {
        "page-size": "Letter",
        "encoding": "UTF-8",
    }

    # Configurar wkhtmltopdf
    config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")

    # Convertir el HTML en un PDF
    pdf = pdfkit.from_string(html, False, options=options, configuration=config)

    # Devolver el PDF como respuesta
    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="programacion.pdf"'
    return response
