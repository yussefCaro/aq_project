from django.urls import path
from .views import listado_solicitudes
from . import views

urlpatterns = [
    path('solicitudes/', listado_solicitudes, name='listado_solicitudes'),
    path('solicitudes/', views.listado_solicitudes, name='listado_solicitudes'),
    path('solicitud/<int:solicitud_id>/cambiar_estado/', views.cambiar_estado, name='cambiar_estado'),

]
