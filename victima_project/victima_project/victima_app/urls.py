from . import views
from django.urls import path
from .views import lista_beneficiario  # Importa la vista que deseas usar

urlpatterns = [
    # Define your URL patterns here
    # Example:
    path('lista-beneficiario/', lista_beneficiario, name='example'),
    #path('', views.home, name='home'),
    #path('detalle/<int:id>/', views.detalle, name='detalle'),
    #path('crear/', views.crear, name='crear'),
    #path('editar/<int:id>/', views.editar, name='editar'),
    #path('eliminar/<int:id>/', views.eliminar, name='eliminar'),
]