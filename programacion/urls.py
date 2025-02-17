from django.urls import path
from . import views  # Importamos las vistas correctamente

urlpatterns = [
    path('cotizaciones/', views.listado_cotizaciones, name='listado_cotizaciones'),  # Se cambia a listado_cotizaciones
    path('cotizacion/<int:cotizacion_id>/cambiar_estado/', views.cambiar_estado, name='cambiar_estado'),
    path("programaciones/", views.listado_programaciones, name="listado_programaciones"),
    path("imprimir/<int:programacion_id>/", views.imprimir_programacion, name="imprimir_programacion"),
    path('programar_auditoria/<int:cotizacion_id>/', views.programar_auditoria, name='programar_auditoria'),
    path('crear_programacion/<int:cotizacion_id>/', views.crear_programacion, name='crear_programacion'),

]
