from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from django.contrib.auth.decorators import login_required
from .models import PlanAuditoria, ActaAuditoria, AsistenteActa
from .forms import PlanAuditoriaForm, ActaAuditoriaForm, AsistenteActaForm
from programacion.models import ProgramacionAuditoria, Auditor  # O el nombre real
from datetime import timedelta
from .models import ActividadCEA, HoraActividadPlan
from .forms import HoraActividadPlanFormSet
from django.forms import modelformset_factory
from django.contrib import messages



def auditor_check(user):
    return user.groups.filter(name='Auditores').exists()

@login_required
@user_passes_test(auditor_check)
def dashboard_auditor(request):
    # Obtener el objeto Auditor asociado al usuario logueado
    auditor = Auditor.objects.get(user=request.user)
    # Filtrar programaciones de ese auditor
    programaciones = ProgramacionAuditoria.objects.filter(auditores=auditor)
    # Filtrar planes de auditoría de ese usuario
    planes = PlanAuditoria.objects.filter(auditor=request.user)
    return render(request, 'documentacion_auditores/dashboard.html', {
        'programaciones': programaciones,
        'planes': planes,
    })






from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import PlanAuditoria, ActividadCEA, HoraActividadPlan
from .forms import PlanAuditoriaForm
from django.forms import modelformset_factory
from programacion.models import ProgramacionAuditoria
from datetime import timedelta

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Auditores').exists())
def crear_plan(request, programacion_id):
    programacion = get_object_or_404(ProgramacionAuditoria, id=programacion_id)

    # Verifica si ya existe un plan para esta programación
    plan_existente = PlanAuditoria.objects.filter(programacion=programacion).first()
    if plan_existente:
        messages.info(request, "Ya existe un plan para esta programación. Puedes editarlo aquí.")
        return redirect('editar_plan', plan_existente.id)

    actividades = list(ActividadCEA.objects.filter(nivel=programacion.nivel_auditoria))
    fechas_etapa2 = list(programacion.fechas_etapa2.all())
    fechas_disponibles = [f.fecha for f in fechas_etapa2]

    # Para depuración
    print(f"Actividades: {len(actividades)}")
    print(f"Fechas disponibles: {fechas_disponibles}")

    if request.method == 'POST':
        print("POST recibido")
        form = PlanAuditoriaForm(request.POST, request.FILES)
        formset_factory = modelformset_factory(
            HoraActividadPlan,
            fields=('fecha', 'hora'),
            extra=len(actividades)
        )
        formset = formset_factory(request.POST)
        print("Form válido:", form.is_valid())
        print("Formset válido:", formset.is_valid())
        print("Form errors:", form.errors)
        print("Formset errors:", formset.errors)
        if form.is_valid() and formset.is_valid():
            print("Guardando plan...")
            plan = form.save(commit=False)
            plan.programacion = programacion
            plan.auditor = request.user
            if fechas_etapa2:
                plan.fecha_aprobacion = fechas_etapa2[0].fecha - timedelta(days=2)
            else:
                from django.utils import timezone
                plan.fecha_aprobacion = timezone.now().date()
            plan.save()
            for subform, actividad in zip(formset, actividades):
                hora_actividad = subform.save(commit=False)
                hora_actividad.plan = plan
                hora_actividad.actividad = actividad
                hora_actividad.save()
            messages.success(request, "Plan de auditoría creado correctamente.")
            return redirect('dashboard_auditor')
        else:
            messages.error(request, "Corrige los errores en el formulario.")
    else:
        form = PlanAuditoriaForm()
        formset_factory = modelformset_factory(
            HoraActividadPlan,
            fields=('fecha', 'hora'),
            extra=len(actividades)
        )
        formset = formset_factory(queryset=HoraActividadPlan.objects.none())

    return render(request, 'documentacion_auditores/plan_form.html', {
        'form': form,
        'formset': formset,
        'actividades': actividades,
        'fechas_disponibles': fechas_disponibles,
        'programacion': programacion,
    })




@login_required
@user_passes_test(lambda u: u.groups.filter(name='Auditores').exists())
def editar_plan(request, plan_id):
    plan = get_object_or_404(PlanAuditoria, id=plan_id)
    actividades = list(ActividadCEA.objects.filter(nivel=plan.programacion.nivel_auditoria))
    fechas_etapa2 = list(plan.programacion.fechas_etapa2.all())
    fechas_disponibles = [f.fecha for f in fechas_etapa2]

    queryset_horas = HoraActividadPlan.objects.filter(plan=plan)
    if queryset_horas.exists():
        extra_forms = 0
    else:
        extra_forms = len(actividades)

    formset_factory = modelformset_factory(
        HoraActividadPlan,
        fields=('fecha', 'hora'),
        extra=extra_forms
    )

    if request.method == 'POST':
        form = PlanAuditoriaForm(request.POST, request.FILES, instance=plan)
        formset = formset_factory(request.POST, queryset=queryset_horas)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('dashboard_auditor')
    else:
        form = PlanAuditoriaForm(instance=plan)
        formset = formset_factory(queryset=queryset_horas)

    return render(request, 'documentacion_auditores/plan_form.html', {
        'form': form,
        'formset': formset,
        'actividades': actividades,
        'fechas_disponibles': fechas_disponibles,
        'programacion': plan.programacion,
        'editando': True,
    })



@login_required
@user_passes_test(auditor_check)
def crear_acta(request, programacion_id):
    programacion = get_object_or_404(ProgramacionAuditoria, id=programacion_id)
    if request.method == 'POST':
        form = ActaAuditoriaForm(request.POST, request.FILES)
        if form.is_valid():
            acta = form.save(commit=False)
            acta.programacion = programacion
            acta.save()
            return redirect('dashboard_auditor')
    else:
        form = ActaAuditoriaForm()
    return render(request, 'documentacion_auditores/acta_form.html', {'form': form, 'programacion': programacion})

@login_required
@user_passes_test(auditor_check)
def imprimir_plan(request, plan_id):
    plan = get_object_or_404(PlanAuditoria, id=plan_id)
    programacion = plan.programacion
    hora_actividades = plan.horas_actividades.all().order_by('fecha', 'hora')
    html_string = render_to_string(
        'documentacion_auditores/plan_pdf.html',
        {
            'plan': plan,
            'programacion': programacion,
            'hora_actividades': hora_actividades,
        }
    )
    html = HTML(string=html_string)
    pdf_file = html.write_pdf()
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'filename=PlanAuditoria_{programacion.cotizacion.numero_servicio}.pdf'
    return response



@login_required
@user_passes_test(auditor_check)
def imprimir_acta(request, acta_id):
    acta = get_object_or_404(ActaAuditoria, id=acta_id)
    html_string = render_to_string('documentacion_auditores/acta_pdf.html', {'acta': acta})
    html = HTML(string=html_string)
    pdf_file = html.write_pdf()
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'filename=ActaAuditoria_{acta.programacion.cotizacion.numero_servicio}.pdf'
    return response



@login_required
def imprimir_programacion(request, programacion_id):
    programacion = ProgramacionAuditoria.objects.get(id=programacion_id)
    html_string = render_to_string('documentacion_auditores/programacion_pdf.html', {
        'programacion': programacion
    })
    pdf_file = HTML(string=html_string).write_pdf()
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'filename=programacion_{programacion.id}.pdf'
    return response
