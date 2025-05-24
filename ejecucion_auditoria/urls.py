from django.urls import path
from . import views

urlpatterns = [
    path('acta/<int:acta_id>/ejecucion/', views.ejecucion_auditoria, name='ejecucion_auditoria'),
    path('ejecucion/acta/<int:acta_id>/subsanacion/', views.subsanacion_no_conformidades, name='subsanacion_no_conformidades'),
    path('ejecucion/acta/<int:acta_id>/finalizar_subsanacion/', views.finalizar_subsanacion, name='finalizar_subsanacion'),
    path('ejecucion/acta/<int:acta_id>/reporte/', views.reporte_auditoria, name='reporte_auditoria'),


]
