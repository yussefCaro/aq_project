from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_auditor, name='dashboard_auditor'),
    path('plan/<int:programacion_id>/', views.crear_plan, name='crear_plan'),
    path('acta/<int:programacion_id>/', views.crear_acta, name='crear_acta'),
    path('plan/<int:plan_id>/imprimir/', views.imprimir_plan, name='imprimir_plan'),
    path('acta/<int:acta_id>/imprimir/', views.imprimir_acta, name='imprimir_acta'),


]