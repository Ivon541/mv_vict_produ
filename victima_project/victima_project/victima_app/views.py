from django.shortcuts import render
from django.views.generic import ListView
from .models import Beneficiarios
from django.http import HttpResponse

class BeneficiarioListView(ListView):
    model = Beneficiarios
    template_name = 'lista_beneficiarios.html'
    context_object_name = 'beneficiarios'
    paginate_by = 10  # Número de beneficiarios por página

    def get_queryset(self):
        return Beneficiarios.objects.filter(es_victima_conflicto=True)
    
def lista_beneficiario(request):
    beneficiarios = Beneficiarios.objects.all()
    return render(request, 'victima_app/lista_beneficiarios.html', {'beneficiarios': beneficiarios}) 
