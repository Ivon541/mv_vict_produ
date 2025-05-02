from django.shortcuts import render
from victima_app.models import Contratos
from victima_app.models import Beneficiarios
#from .forms import BeneficiarioForm 
#from .forms import BeneficiarioForm


# Crear en django una vista que muestre un listado de contratos
def contract_list(request):
    # Aquí iría la lógica para obtener los contratos de la base de datos
    contrato = Contratos.objects.all()  # Obtener los contratos de la base de datos
    context = {
        'contratos': contrato  # Pasar los contratos al contexto
    }
    return render(request, 'victima/lista_contratos.html', context)  # Renderizar la plantilla con el contexto

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




