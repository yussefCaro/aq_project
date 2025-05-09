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

@login_required
@user_passes_test(auditor_check)
def crear_plan(request, programacion_id):
    programacion = get_object_or_404(ProgramacionAuditoria, id=programacion_id)
    if request.method == 'POST':
        form = PlanAuditoriaForm(request.POST, request.FILES)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.programacion = programacion
            plan.auditor = request.user

            # Obtener la primera fecha de etapa 2 si existe
            primera_fecha_etapa2 = programacion.fechas_etapa2.first()
            if primera_fecha_etapa2:
                plan.fecha_aprobacion = primera_fecha_etapa2.fecha - timedelta(days=2)
            else:
                plan.fecha_aprobacion = None  # O maneja el caso como prefieras

            plan.save()
            return redirect('dashboard_auditor')
    else:
        form = PlanAuditoriaForm()
    return render(request, 'documentacion_auditores/plan_form.html', {'form': form, 'programacion': programacion})


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
    html_string = render_to_string('documentacion_auditores/plan_pdf.html', {'plan': plan})
    html = HTML(string=html_string)
    pdf_file = html.write_pdf()
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'filename=PlanAuditoria_{plan.programacion.cotizacion.numero_servicio}.pdf'
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
