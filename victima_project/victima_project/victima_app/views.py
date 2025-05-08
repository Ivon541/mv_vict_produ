from django.shortcuts import render, redirect
from victima_app.models import Contratos, Usuario
from victima_app.models import Beneficiarios
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets
from .serializers import UsuarioSerializer, ContratosSerializer
from django.contrib.auth.decorators import login_required
#from .forms import BeneficiarioForm 
#from .forms import BeneficiarioForm


# Crear en django una vista que muestre un listado de contratos
def contrato_list(request):
    pass
    contratos = Contratos.objects.all()  # Obtener los contratos de la base de datos
    context = {
        'contratos': contratos  # Pasar los contratos al contexto
    }
    if request.user.is_authenticated:
        return render(request, 'victima_app/lista_contratos.html', context)  # Renderizar la plantilla con el contexto
    else:
        return HttpResponseRedirect(reverse("login"))
    

# Crear en django una vista para almacenar en la base de datos un contrato

def crear_contrato(request):
    
    beneficiarios = Beneficiarios.objects.all()  # Obtener todos los beneficiarios
    if request.method == 'POST':
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        etapa = request.POST.get('etapa')
        beneficiarios = Beneficiarios.objects.all()  # Obtener todos los beneficiarios
        beneficiarios_ids = [beneficiario.id_beneficiario for beneficiario in beneficiarios]  # Extraer los IDs
        Contratos.objects.create(
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            etapa=etapa,
            id_beneficiario_id=beneficiarios_ids[0]  # Asignar el primer beneficiario como ejemplo
        )
        return HttpResponseRedirect(reverse("contrato_list"))
    context = {
        'beneficiarios': beneficiarios  # Pasar los beneficiarios al contexto
    }
    if request.user.is_authenticated:
        return render(request, 'victima_app/crear_contratos.html', context)  # Renderizar la plantilla para crear un contrato
    else:
        return HttpResponseRedirect(reverse("login"))
    

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

class ContratosViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Contratos.objects.all()
    serializer_class = ContratosSerializer
    permission_classes = [permissions.IsAuthenticated]


class UsuarioViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.IsAuthenticated]



def buscar_beneficiario(request):
    query = request.GET.get('q')  # Obtener el término de búsqueda desde el parámetro 'q'
    if query:
        beneficiarios = Beneficiarios.objects.filter(nombre__icontains=query)  # Filtrar beneficiarios por nombre
    else:
        beneficiarios = Beneficiarios.objects.all()  # Mostrar todos los beneficiarios si no hay búsqueda
    context = {
        'beneficiarios': beneficiarios,  # Pasar los beneficiarios al contexto
        'query': query  # Pasar el término de búsqueda al contexto
    }
    return render(request, 'victima_app/lista_contratos.html', context)  # Renderizar la plantilla con el contexto


def detalle_beneficiario(request, beneficiario_id):
    beneficiario = Beneficiarios.objects.get(id=beneficiario_id)  # Obtener el beneficiario por ID
    context = {
        'beneficiario': beneficiario  # Pasar el beneficiario al contexto
        }
    return render(request, 'victima_app/detalle_beneficiario.html', context)  # Renderizar la plantilla con el contexto

def editar_contrato(request, id_contrato):
    contrato = Contratos.objects.get(pk=id_contrato)  # Obtener el contrato por ID

    if request.method == 'POST':
        contrato.fecha_inicio = request.POST.get('fecha_inicio')
        contrato.fecha_fin = request.POST.get('fecha_fin')
        contrato.etapa = request.POST.get('etapa')
        contrato.save()  # Guardar los cambios en la base de datos
        return redirect('contrato_list')  # Redirigir a la lista de contratos

    context = {
        'contrato': contrato  # Pasar el contrato al contexto
    }
    return render(request, 'victima_app/editar_contrato.html', context)  # Renderizar la plantilla para editar un contrato


def eliminar_contrato(request, id_contrato):
    contrato = Contratos.objects.get(pk=id_contrato)  # Obtener el contrato por ID

    if request.method == 'POST':
        contrato.delete()  # Eliminar el contrato de la base de datos
        return redirect('contrato_list')  # Redirigir a la lista de contratos

    context = {
        'contrato': contrato  # Pasar el contrato al contexto
    }
    return render(request, 'victima_app/eliminar_contrato.html', context)  # Renderizar la plantilla para confirmar la eliminación




