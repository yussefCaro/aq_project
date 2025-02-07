from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Solicitud, Programacion
from .forms import ProgramacionForm
from solicitudes.models import Solicitud  # Parece que esto ya está importado arriba, puedes eliminar la repetición


@login_required
def listado_solicitudes(request):
    solicitudes = Solicitud.objects.filter(estado='Pendiente')  # Solo solicitudes pendientes
    usuarios = User.objects.all()  # Obtener la lista de usuarios para asignar auditores

    if request.method == "POST":
        solicitud_id = request.POST.get('solicitud_id')
        fecha_auditoria = request.POST.get('fecha_auditoria')
        auditor_id = request.POST.get('auditor')

        solicitud = get_object_or_404(Solicitud, id=solicitud_id)
        auditor = get_object_or_404(User, id=auditor_id)

        # Crear o actualizar la programación
        programacion, created = Programacion.objects.get_or_create(solicitud=solicitud)
        programacion.fecha_auditoria = fecha_auditoria
        programacion.auditor = auditor
        programacion.save()

        # Cambiar estado de la solicitud a 'Programada'
        solicitud.estado = 'Programada'
        solicitud.save()

        return redirect('listado_solicitudes')

    return render(request, 'programacion/listado.html', {'solicitudes': solicitudes, 'usuarios': usuarios})


@login_required
def cambiar_estado(request, solicitud_id):
    solicitud = get_object_or_404(Solicitud, id=solicitud_id)
    solicitud.estado = 'Programada'  # Cambia el estado a 'Programada'
    solicitud.save()  # Guarda el cambio
    return redirect('listado_solicitudes')  # Redirige al listado de solicitudes
