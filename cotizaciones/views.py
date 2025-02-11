from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from solicitudes.models import Solicitud
from .models import Cotizacion, TipoServicio
from .forms import CotizacionForm
from decimal import Decimal
from django.utils.formats import localize


@login_required
def listado_solicitudes(request):
    """ Muestra las solicitudes pendientes para cotización """
    solicitudes = Solicitud.objects.filter(estado="Pendiente").select_related("cliente")  # Optimización con select_related
    return render(request, "cotizaciones/listado_solicitudes.html", {"solicitudes": solicitudes})




@login_required
def crear_cotizacion(request, solicitud_id):
    solicitud = get_object_or_404(Solicitud, id=solicitud_id)

    if request.method == "POST":
        form = CotizacionForm(request.POST)
        if form.is_valid():
            numero_servicio = form.cleaned_data["numero_servicio"]

            # Verificar si ya existe una cotización con el mismo número
            if Cotizacion.objects.filter(numero_servicio=numero_servicio).exists():
                return HttpResponseBadRequest("Error: Este número de servicio ya existe.")

            # Crear la cotización
            cotizacion = form.save(commit=False)
            cotizacion.solicitud = solicitud
            cotizacion.save()

            # Cambiar estado de la solicitud
            solicitud.estado = "Cotizada"
            solicitud.save()

            return redirect("listado_cotizaciones")  # Redirigir a la lista de cotizaciones

    else:
        form = CotizacionForm()

    return render(request, "cotizaciones/crear_cotizacion.html", {"form": form, "solicitud": solicitud})



@login_required
def listado_cotizaciones(request):
    """ Muestra la lista de cotizaciones creadas """
    cotizaciones = Cotizacion.objects.all()
    return render(request, "cotizaciones/listado_cotizaciones.html", {"cotizaciones": cotizaciones})

@login_required
def detalle_cotizacion(request, cotizacion_id):
    """ Muestra el detalle de una cotización """
    cotizacion = get_object_or_404(Cotizacion, id=cotizacion_id)
    # Formatear los valores como moneda
    cotizacion.precio_neto = localize(cotizacion.precio_neto)
    cotizacion.precio_iva = localize(cotizacion.precio_iva)
    cotizacion.precio_total = localize(cotizacion.precio_total)

    return render(request, "cotizaciones/detalle_cotizacion.html", {"cotizacion": cotizacion})

@login_required
def solicitudes_pendientes(request):
    solicitudes = Solicitud.objects.filter(estado="Pendiente")
    return render(request, "solicitudes/pendientes.html", {"solicitudes": solicitudes})


@login_required
def editar_cotizacion(request, cotizacion_id):
    cotizacion = get_object_or_404(Cotizacion, id=cotizacion_id)

    if request.method == "POST":
        form = CotizacionForm(request.POST, instance=cotizacion)
        if form.is_valid():
            cotizacion = form.save(commit=False)
            cotizacion.precio_iva = Decimal(request.POST.get("precio_iva", 0))
            cotizacion.precio_total = Decimal(request.POST.get("precio_total", 0))
            cotizacion.save()
            return redirect("listado_cotizaciones")

    else:
        form = CotizacionForm(instance=cotizacion)

    return render(request, "cotizaciones/editar_cotizacion.html", {"form": form, "cotizacion": cotizacion})


