from django.urls import path
from . import views

urlpatterns = [
    path('turnos/', views.ver_turnos, name='ver_turnos'),
    path('turnos/agregar/', views.agregar_turno, name='agregar_turno'),
    path('turnos/atender/', views.atender_turno, name='atender_turno'),
    path('historial/', views.ver_historial, name='ver_historial'),
    path('historial/deshacer/', views.deshacer_ultima_accion, name='deshacer_accion'),
]
