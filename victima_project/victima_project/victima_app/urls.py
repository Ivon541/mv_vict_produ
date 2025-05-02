from django.urls import path
from .views import lista_beneficiario  # Importa la vista que deseas usar

urlpatterns = [
    # Define your URL patterns here
    # Example:
    path('lista-beneficiario/', lista_beneficiario, name='example'),
]