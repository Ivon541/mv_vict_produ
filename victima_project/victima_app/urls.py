from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views
from django.urls import path
from .views import beneficiary_list, crear_beneficiario, eliminar_beneficiario # Importa la vista que deseas usar


urlpatterns = [
    path('contratos/', views.contrato_list, name='contrato_list'),  # Listar contratos
    path('crear-contrato/', views.crear_contrato, name='crear_contrato'),  # Crear contrato
    path('crear-beneficiario/', views.crear_beneficiario, name='crear_beneficiario'),  # Crear beneficiario
    path('beneficiarios/', views.contrato_list, name='beneficiario_list'),  # Listar contratos
    path('eliminar-beneficiario/<int:id_beneficiario>/', views.eliminar_beneficiario, name='eliminar_beneficiario'),  # Eliminar beneficiario
    path('editar-beneficiario/<int:id_beneficiario>/', views.editar_beneficiario, name='editar_beneficiario'),  # Editar beneficiario
    path('buscar_beneficiario/', views.buscar_beneficiario, name='buscar_beneficiario'),  # Buscar beneficiario
    path('detalle_beneficiario/<int:id>/', views.detalle_beneficiario, name='detalle_beneficiario'),  # Detalle beneficiario
    path('lista-beneficiarios/', views.beneficiary_list, name='lista_beneficiarios'),  # Listar beneficiarios
    path('editar_contrato/<int:id_contrato>/', views.editar_contrato, name='editar_contrato'),  # Editar contrato
    path('eliminar_contrato/<int:id_contrato>/', views.eliminar_contrato, name='eliminar_contrato'),  # Eliminar contrato
    path('crear-programas/', views.crear_programa, name='crear_programas'),  # Crear programa
    path('lista-programas/', views.lista_programas, name='lista_programas'),  # Lista programa
    path('editar-programa/<int:id_programa>/', views.editar_programa, name='editar_programa'),
    path('eliminar-programa/<int:id_programa>/', views.eliminar_programa, name='eliminar_programa'),  # Eliminar programa
    path('lista-entregas/', views.lista_entregas, name='lista_entregas'),  # Lista entregas
    path('crear-entregas/', views.crear_entrega, name='crear_entregas'),  # Crear programa
    path('eliminar-entrega/<int:id_entrega>/', views.eliminar_entrega, name='eliminar_entrega'),
    path('editar-entrega/<int:id_entrega>/', views.editar_entrega, name='editar_entrega'),  # Editar entrega
    path('consultar-programa/', views.consultar_programa, name='consultar_programas'),  # Consultar programa
    #path('', views.home, name='home'),
    #path('detalle/<int:id>/', views.detalle, name='detalle'),
    #path('crear/', views.crear, name='crear'),
    #path('editar/<int:id>/', views.editar, name='editar'),
    #path('eliminar/<int:id>/', views.eliminar, name='eliminar'),
] 