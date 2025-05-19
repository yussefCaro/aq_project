from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.shortcuts import get_object_or_404, redirect, render

from documentacion_auditores.models import ActaAuditoria
from ejecucion_auditoria.models import RequisitoAuditoria, EjecucionRequisito




@login_required
def ejecucion_auditoria(request, acta_id):
    acta = get_object_or_404(ActaAuditoria, id=acta_id)
    requisitos = RequisitoAuditoria.objects.all()
    EjecucionFormSet = modelformset_factory(
        EjecucionRequisito,
        fields=[
            'cumple', 'no_cumple', 'no_aplica',
            'aspecto_mejora', 'concepto_mejora',
            'concepto_no_conformidad', 'evidencia',
            'concepto_evidencia', 'imagen1', 'imagen2'
        ],
        extra=0,
        can_delete=False
    )
    queryset = EjecucionRequisito.objects.filter(acta=acta).order_by('requisito__id')
    if request.method == 'POST':
        formset = EjecucionFormSet(request.POST, request.FILES, queryset=queryset)
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.acta = acta
                instance.save()
            # Validar que todos los requisitos estén diligenciados antes de finalizar
            if 'finalizar' in request.POST:
                # Aquí va la lógica de finalización
                pass
            # Puedes mostrar un mensaje de éxito aquí si quieres
            return redirect('ejecucion_auditoria', acta_id=acta.id)
    else:
        if not queryset.exists():
            for req in requisitos:
                EjecucionRequisito.objects.create(acta=acta, requisito=req)
        formset = EjecucionFormSet(queryset=EjecucionRequisito.objects.filter(acta=acta).order_by('requisito__id'))
    return render(request, 'ejecucion_auditoria/ejecucion_auditoria.html', {
        'acta': acta,
        'formset': formset,
    })
