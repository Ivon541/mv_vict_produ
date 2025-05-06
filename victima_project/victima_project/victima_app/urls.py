from . import views
from django.urls import path
from .views import lista_beneficiario, update_beneficiary, beneficiary_list # Importa la vista que deseas usar


urlpatterns = [
    path('contratos/', views.contrato_list, name='contrato_list'),  # Listar contratos
    path('crear-contrato/', views.crear_contrato, name='crear_contrato'),  # Crear contrato
    path('crear-beneficiario/', views.crear_beneficiario, name='crear_beneficiarios'),  # Crear beneficiario
    path('lista_beneficiario/', views. beneficiary_list, name='lista_beneficiarios'),
    path('beneficiarios/', views.contrato_list, name='beneficiario_list'), 
    path('beneficiario/', views.update_beneficiary, name='update_beneficiary'),# Eliminar beneficiario
    path('crear-entregas/', views.crear_entregas, name='crear_entregas'),  # Listar entregas
    path('entregas/', views.entregas_list, name='entregas_list'),  # Listar entregas
    #path('', views.home, name='home'),
    #path('detalle/<int:id>/', views.detalle, name='detalle'),
    #path('crear/', views.crear, name='crear'),
    #path('editar/<int:id>/', views.editar, name='editar'),
    #path('eliminar/<int:id>/', views.eliminar, name='eliminar'),
]