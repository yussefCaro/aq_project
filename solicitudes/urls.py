from django.urls import path
from . import views

urlpatterns = [
    path('solicitud/', views.solicitud, name='solicitud'),
    path('clientes/solicitud/pdf/<int:cliente_id>/', views.generar_solicitud_pdf, name='generar_solicitud_pdf'),

]
