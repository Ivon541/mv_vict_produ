from django.shortcuts import render, redirect
from victima_app.models import Contratos
from victima_app.models import Beneficiarios
from django.http import HttpResponseRedirect
from django.urls import reverse
#from .forms import BeneficiarioForm 
#from .forms import BeneficiarioForm


# Crear en django una vista que muestre un listado de contratos
def contrato_list(request):
    contratos = Contratos.objects.all()  # Obtener los contratos de la base de datos
    context = {
        'contratos': contratos  # Pasar los contratos al contexto
    }
    return render(request, 'victima_app/lista_contratos.html', context)  # Renderizar la plantilla con el contexto

# Crear en django una vista para almacenar en la base de datos un contrato
def crear_contrato(request):
    if request.method == 'POST':
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        etapa = request.POST.get('etapa')
        beneficiarios = Beneficiarios.objects.all()  # Obtener todos los beneficiarios
        beneficiarios_ids = [beneficiario.id for beneficiario in beneficiarios]  # Extraer los IDs
        Contratos.objects.create(
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            etapa=etapa,
            id_beneficiario_id=beneficiarios_ids[0]  # Asignar el primer beneficiario como ejemplo
        )
        return HttpResponseRedirect(reverse("login"))
    return render(request, 'victima_app/crear_contratos.html')  # Renderizar la plantilla para crear un contrato

def crear_beneficiario(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        documento_identidad = request.POST.get('documento_identidad')
        Beneficiarios.objects.create(
            nombre=nombre,
            documento_identidad=documento_identidad
        )
        return HttpResponseRedirect(reverse("beneficiario_list"))  # Redirigir a la lista de beneficiarios después de crear uno
    return render(request, 'victima_app/crear_beneficiario.html')  # Renderizar la plantilla para crear un contrato

# Crear en django una vista que muestre un listado de   beneficiarios
def beneficiary_list(request):
    # Aquí iría la lógica para obtener los beneficiarios de la base de datos
    beneficiario = Beneficiarios.objects.all()  # Obtener los beneficiarios de la base de datos
    context = {
        'beneficiarios': beneficiario  # Pasar los beneficiarios al contexto
    }
    return render(request, 'victima/lista_beneficiarios.html', context)  # Renderizar la plantilla con el contexto

#Crear en django una vista  para almacenar en la base de  datos  un beneficiario
def create_beneficiary(request):
    if request.method == 'POST':
        form = BeneficiarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_beneficiarios')  # Redirige a una vista adecuada
    else:
        form = BeneficiarioForm()

    return render(request, 'victima/crear_beneficiario.html', {'form': form}) # Renderizar la plantilla para crear un beneficiario


# Crear en django una vista  para eliminar un beneficiario de la base de datos
def update_beneficiary(request, beneficiary_id):
    beneficiario = get_object_or_404(Beneficiario, id=beneficiary_id)  # Obtén el beneficiario de la BD

    if request.method == 'POST':
        form = BeneficiarioForm(request.POST, instance=beneficiario)  # Cargar datos en el formulario
        if form.is_valid():
            form.save()
            return redirect('lista_beneficiarios')  # Redirige después de la actualización
    else:
        form = BeneficiarioForm(instance=beneficiario)  # Mostrar datos actuales en el formulario

    return render(request, 'victima/actualizar_beneficiario.html', {'form': form, 'beneficiario': beneficiario}) # Renderizar la plantilla para actualizar un beneficiario



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
