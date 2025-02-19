from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template.loader import render_to_string
import json
import pdfkit
from cotizaciones.models import Cotizacion

from .forms import ProgramacionAuditoriaForm

from .models import ProgramacionAuditoria
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import ProgramacionAuditoria, Auditor, FechaEtapa2
from .forms import ProgramacionAuditoriaForm, FechaEtapa2FormSet



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
    cotizaciones = Cotizacion.objects.filter(estado="Pendiente")
    usuarios = User.objects.all()  # Auditores disponibles

    if request.method == "POST":
        cotizacion_id = request.POST.get("cotizacion_id")
        fecha_etapa_1 = request.POST.get("fecha_etapa_1")
        hora_etapa_1 = request.POST.get("hora_etapa_1")
        fecha_etapa_2 = request.POST.get("fecha_etapa_2")
        hora_etapa_2 = request.POST.get("hora_etapa_2")
        auditor_id = request.POST.get("auditor")

        cotizacion = get_object_or_404(Cotizacion, id=cotizacion_id)
        auditor = get_object_or_404(User, id=auditor_id)

        # Crear o actualizar la programación
        programacion, created = ProgramacionAuditoria.objects.get_or_create(cotizacion=cotizacion)

        # Asignar las fechas y horas a la programación
        programacion.fecha_etapa_1 = fecha_etapa_1
        programacion.hora_etapa_1 = hora_etapa_1
        programacion.fecha_etapa_2 = fecha_etapa_2
        programacion.hora_etapa_2 = hora_etapa_2
        programacion.auditor = auditor

        # Cambiar estado de la cotización
        cotizacion.estado = "Programada"
        cotizacion.save()

        programacion.save()

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
    """ Muestra la lista de programaciones de auditoría. """
    programaciones = ProgramacionAuditoria.objects.select_related("cotizacion").filter(estado="Programada")

    # Obtener los grupos del usuario
    grupos_usuario = request.user.groups.values_list("name", flat=True)

    contexto = {
        "programaciones": programaciones,
        "pertenece_comercial": "Comercial" in grupos_usuario,
        "pertenece_programacion": "Programación" in grupos_usuario,  # Asegúrate de que el nombre del grupo es correcto
    }

    return render(request, "programacion/listado_programaciones.html", contexto)

@login_required
def imprimir_programacion(request, programacion_id):
    """ Genera un PDF con la programación de auditoría. """
    programacion = get_object_or_404(ProgramacionAuditoria, id=programacion_id)

    # Convertir la cadena JSON a lista si es necesario
    if isinstance(programacion.fecha_programacion_etapa2, str):
        programacion.fecha_programacion_etapa2 = json.loads(programacion.fecha_programacion_etapa2)

    # Renderizar la plantilla
    html = render_to_string("programacion/imprimir.html", {"programacion": programacion})

    # Opciones de pdfkit
    options = {
        "page-size": "Letter",
        "encoding": "UTF-8",
    }

    # Configurar wkhtmltopdf
    config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")

    # Generar PDF
    pdf = pdfkit.from_string(html, False, options=options, configuration=config)

    # Respuesta con PDF
    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="programacion.pdf"'
    return response


@login_required
def programar_auditoria(request, cotizacion_id):
    cotizacion = get_object_or_404(Cotizacion, id=cotizacion_id)
    programacion, created = ProgramacionAuditoria.objects.get_or_create(cotizacion=cotizacion)

    if request.method == 'POST':
        form = ProgramacionAuditoriaForm(request.POST, instance=programacion)
        fecha_formset = FechaEtapa2FormSet(request.POST, instance=programacion)

        if form.is_valid() and fecha_formset.is_valid():
            programacion = form.save()
            fecha_formset.save()
            return redirect('listado_programaciones')
    else:
        form = ProgramacionAuditoriaForm(instance=programacion)
        fecha_formset = FechaEtapa2FormSet(instance=programacion)

    return render(request, 'programacion/form_programacion.html', {
        'form': form,
        'fecha_formset': fecha_formset,
        'cotizacion': cotizacion,
        'titulo': 'Programar Auditoría',
        'boton_texto': 'Guardar Programación'
    })


@login_required
def crear_programacion(request, cotizacion_id=None):
    cotizacion = None
    if cotizacion_id:
        cotizacion = get_object_or_404(Cotizacion, id=cotizacion_id)

    if request.method == "POST":
        form = ProgramacionAuditoriaForm(request.POST)
        if form.is_valid():
            programacion = form.save(commit=False)
            if cotizacion:
                programacion.cotizacion = cotizacion
            programacion.save()
            form.save_m2m()  # Guardar relaciones ManyToMany
            return redirect("listado_programaciones")
    else:
        form = ProgramacionAuditoriaForm()

    return render(request, "programacion/form_programacion.html", {"form": form, "cotizacion": cotizacion})

