from django.urls import path
from . import views

urlpatterns = [
    path('solicitud/', views.solicitud, name='solicitud'),
    path('clientes/ver/<int:cliente_id>/', views.ver_cliente, name='ver_cliente'),
    path('clientes/editar/<int:cliente_id>/', views.editar_cliente, name='editar_cliente'),
    path('clientes/crear/<str:nit>/', views.crear_cliente, name='crear_cliente'),
    path('clientes/solicitud/pdf/<int:cliente_id>/', views.generar_solicitud_pdf, name='generar_solicitud_pdf'),

]
