from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.contrib import messages
from datetime import date

from .forms import EjecucionBaseFormSet, EjecucionRequisitoForm
from documentacion_auditores.models import ActaAuditoria
from ejecucion_auditoria.models import RequisitoAuditoria, EjecucionRequisito

@login_required
def ejecucion_auditoria(request, acta_id):
    acta = get_object_or_404(ActaAuditoria, id=acta_id)
    requisitos = RequisitoAuditoria.objects.all()
    queryset = EjecucionRequisito.objects.filter(acta=acta).order_by('requisito__id')

    EjecucionFormSet = modelformset_factory(
        EjecucionRequisito,
        fields=[
            'cumple', 'no_cumple', 'no_aplica',
            'aspecto_mejora', 'concepto_mejora',
            'concepto_no_conformidad', 'evidencia',
            'concepto_evidencia', 'imagen1', 'imagen2'
        ],
        extra=0,
        can_delete=False,
        formset=EjecucionBaseFormSet
    )

    # SOLO crear los registros si no existen (solo la primera vez)
    if not queryset.exists():
        for req in requisitos:
            EjecucionRequisito.objects.create(acta=acta, requisito=req)
        queryset = EjecucionRequisito.objects.filter(acta=acta).order_by('requisito__id')

    if request.method == 'POST':
        # --- NUEVO BLOQUE: Manejo de recomendaciones ---
        recomendaciones = request.POST.get('recomendaciones')
        if recomendaciones:
            acta.recomendaciones = recomendaciones
            acta.save()
            messages.success(request, "¡Recomendación guardada exitosamente!")
            return redirect('reporte_auditoria', acta_id=acta.id)
        # --- FIN BLOQUE NUEVO ---

        formset = EjecucionFormSet(request.POST, request.FILES, queryset=queryset)
        if 'finalizar' in request.POST:
            formset.validar_completo = True

        if formset.is_valid():
            formset.save()
            if 'finalizar' in request.POST:
                hay_no_conformidades = any(
                    form.cleaned_data.get('no_cumple') for form in formset.forms
                )
                if hay_no_conformidades:
                    if not acta.fecha_inicio_subsanacion:
                        acta.fecha_inicio_subsanacion = timezone.now().date()
                        acta.save()
                    request.session['mensaje_subsanacion'] = (
                        "Existen no conformidades pendientes por subsanar. "
                        "Tiene 90 días para realizarlo."
                    )
                    return redirect('subsanacion_no_conformidades', acta_id=acta.id)
                else:
                    return render(request, 'ejecucion_auditoria/ejecucion_auditoria.html', {
                        'acta': acta,
                        'formset': formset,
                        'mostrar_modal_recomendacion': True,
                    })
            else:
                messages.success(request, "¡Avance guardado exitosamente!")
                return redirect('ejecucion_auditoria', acta_id=acta.id)
        # Si hay errores, el template los mostrará automáticamente
    else:
        formset = EjecucionFormSet(queryset=queryset)

    return render(request, 'ejecucion_auditoria/ejecucion_auditoria.html', {
        'acta': acta,
        'formset': formset,
    })



@login_required
def subsanacion_no_conformidades(request, acta_id):
    acta = get_object_or_404(ActaAuditoria, id=acta_id)
    queryset = EjecucionRequisito.objects.filter(acta=acta, no_cumple=True)

    EjecucionFormSet = modelformset_factory(
        EjecucionRequisito,
        form=EjecucionRequisitoForm,
        fields=[
            'cumple', 'no_cumple', 'no_aplica',
            'aspecto_mejora', 'concepto_mejora',
            'concepto_no_conformidad', 'evidencia',
            'concepto_evidencia', 'imagen1', 'imagen2',
            'subsanado', 'como_se_subsano'
        ],
        extra=0,
        can_delete=False,
    )

    if request.method == 'POST':
        # --- Lógica para guardar recomendación y redirigir al reporte ---
        recomendaciones = request.POST.get('recomendaciones')
        if recomendaciones:
            acta.recomendaciones = recomendaciones
            acta.save()
            messages.success(request, "¡Recomendación guardada exitosamente!")
            return redirect('reporte_auditoria', acta_id=acta.id)
        # --- Fin lógica recomendación ---

        formset = EjecucionFormSet(request.POST, request.FILES, queryset=queryset)
        if formset.is_valid():
            formset.save()
            pendientes_subsanar = formset.queryset.filter(no_cumple=True, subsanado=False).exists()
            dias_restantes = None
            if acta.fecha_inicio_subsanacion:
                dias_restantes = 90 - (date.today() - acta.fecha_inicio_subsanacion).days

            if 'guardar' in request.POST:
                # Solo guardar avances, recarga la página de subsanación
                messages.success(request, "¡Avance guardado exitosamente!")
                return render(request, 'ejecucion_auditoria/subsanacion.html', {
                    'formset': formset,
                    'mensaje': None,
                    'acta': acta,
                    'dias_restantes': dias_restantes,
                    'pendientes_subsanar': pendientes_subsanar,
                })
            # Si no quedan pendientes y no es guardar, redirige a finalizar
            if not pendientes_subsanar:
                return redirect('finalizar_subsanacion', acta_id=acta.id)
            else:
                mensaje = "Aún existen no conformidades pendientes por subsanar."
                messages.warning(request, mensaje)
                return render(request, 'ejecucion_auditoria/subsanacion.html', {
                    'formset': formset,
                    'mensaje': mensaje,
                    'acta': acta,
                    'dias_restantes': dias_restantes,
                    'pendientes_subsanar': pendientes_subsanar,
                })
    else:
        formset = EjecucionFormSet(queryset=queryset)
        pendientes_subsanar = formset.queryset.filter(no_cumple=True, subsanado=False).exists()

    mensaje = request.session.pop('mensaje_subsanacion', None)
    dias_restantes = None
    if acta.fecha_inicio_subsanacion:
        dias_restantes = 90 - (date.today() - acta.fecha_inicio_subsanacion).days

    return render(request, 'ejecucion_auditoria/subsanacion.html', {
        'formset': formset,
        'mensaje': mensaje,
        'acta': acta,
        'dias_restantes': dias_restantes,
        'pendientes_subsanar': pendientes_subsanar,
    })


@login_required
def finalizar_subsanacion(request, acta_id):
    acta = get_object_or_404(ActaAuditoria, id=acta_id)
    if request.method == 'POST':
        recomendaciones = request.POST.get('recomendaciones')
        if recomendaciones:
            acta.recomendaciones = recomendaciones
            acta.save()
            messages.success(request, "¡Recomendación guardada exitosamente!")
            return redirect('reporte_auditoria', acta_id=acta.id)
        else:
            # Si aún no hay recomendación, muestra el modal
            return render(request, 'ejecucion_auditoria/recomendacion.html', {
                'acta': acta,
                'mostrar_modal_recomendacion': True,
            })
    # Si es GET, muestra el modal
    return render(request, 'ejecucion_auditoria/recomendacion.html', {
        'acta': acta,
        'mostrar_modal_recomendacion': True,
    })


@login_required
def reporte_auditoria(request, acta_id):
    acta = get_object_or_404(ActaAuditoria, id=acta_id)
    ejecuciones = EjecucionRequisito.objects.filter(acta=acta).order_by('requisito__id')
    plan = acta.plan
    programacion = plan.programacion
    propietario = plan.programacion.cotizacion.solicitud.cliente.nombre_establecimiento # Ajusta según tus modelos
    return render(request, 'ejecucion_auditoria/reporte_auditoria.html', {
        'acta': acta,
        'plan': plan,
        'programacion': programacion,
        'propietario': propietario,
        'ejecuciones': ejecuciones,
    })




@login_required
def informe_hallazgos(request, acta_id):
    acta = get_object_or_404(ActaAuditoria, id=acta_id)
    ejecuciones = EjecucionRequisito.objects.filter(acta=acta).order_by('requisito__id')
    plan = acta.plan
    programacion = plan.programacion
    return render(request, 'ejecucion_auditoria/informe_hallazgos.html', {
        'acta': acta,
        'plan': plan,
        'programacion': programacion,
        'ejecuciones': ejecuciones,
    })
