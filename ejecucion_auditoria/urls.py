from django.urls import path
from . import views

urlpatterns = [
    path('acta/<int:acta_id>/ejecucion/', views.ejecucion_auditoria, name='ejecucion_auditoria'),
    # ...otras rutas de la app...
]
