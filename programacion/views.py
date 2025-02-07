from django.shortcuts import render, get_object_or_404, redirect
from .models import Solicitud
from django.contrib.auth.decorators import login_required, permission_required

@login_required
def listado_solicitudes(request):
    solicitudes = Solicitud.objects.all()  # Obtiene todas las solicitudes)

    return render(request, 'programacion/listado.html', {'solicitudes': solicitudes})




def cambiar_estado(request, solicitud_id):
    solicitud = get_object_or_404(Solicitud, id=solicitud_id)
    solicitud.estado = 'Programada'  # Cambia el estado a 'Programada'
    solicitud.save()  # Guarda el cambio
    return redirect('listado_solicitudes')  # Redirige al listado de solicitudes
