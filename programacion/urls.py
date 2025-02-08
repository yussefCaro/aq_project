from django.urls import path
from .views import listado_solicitudes
from . import views
from .views import listado_programaciones
from .views import imprimir_programacion


urlpatterns = [
    path('solicitudes/', listado_solicitudes, name='listado_solicitudes'),
    path('solicitudes/', views.listado_solicitudes, name='listado_solicitudes'),
    path('solicitud/<int:solicitud_id>/cambiar_estado/', views.cambiar_estado, name='cambiar_estado'),
    path("programaciones/", listado_programaciones, name="listado_programaciones"),
    path("imprimir/<int:programacion_id>/", imprimir_programacion, name="imprimir_programacion"),


]
