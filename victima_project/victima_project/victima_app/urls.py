from django.urls import path
from . import views

urlpatterns = [
    path('contratos/', views.contrato_list, name='contrato_list'),  # Listar contratos
    path('crear-contrato/', views.crear_contrato, name='crear_contrato'),  # Crear contrato
    path('crear-beneficiario/', views.crear_beneficiario, name='crear_beneficiarios'),  # Crear beneficiario
    path('beneficiarios/', views.contrato_list, name='beneficiario_list'),  # Listar contratos
    path('buscar_beneficiario/', views.buscar_beneficiario, name='buscar_beneficiario'),  # Buscar beneficiario
    path('detalle_beneficiario/<int:id>/', views.detalle_beneficiario, name='detalle_beneficiario'),  # Detalle beneficiario
    path('editar_contrato/<int:id_contrato>/', views.editar_contrato, name='editar_contrato'),  # Editar contrato
    path('eliminar_contrato/<int:id_contrato>/', views.eliminar_contrato, name='eliminar_contrato'),  # Eliminar contrato
    #path('', views.home, name='home'),
    #path('detalle/<int:id>/', views.detalle, name='detalle'),
    #path('crear/', views.crear, name='crear'),
    #path('editar/<int:id>/', views.editar, name='editar'),
    #path('eliminar/<int:id>/', views.eliminar, name='eliminar'),
]