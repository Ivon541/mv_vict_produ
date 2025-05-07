from django.shortcuts import render, redirect
from victima_app.models import Contratos, Usuario
from victima_app.models import Beneficiarios
from victima_app.models import Entregas
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets
from django.views.generic import ListView
from .serializers import UsuarioSerializer, ContratosSerializer
#from .forms import BeneficiarioForm 
#from .forms import BeneficiarioForm


# Crear en django una vista que muestre un listado de contratos
def contrato_list(request):
    pass
    contratos = Contratos.objects.all()  # Obtener los contratos de la base de datos
    context = {
        'contratos': contratos  # Pasar los contratos al contexto
    }
    return render(request, 'victima_app/lista_contratos.html', context)  # Renderizar la plantilla con el contexto

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
    return render(request, 'victima_app/crear_contratos.html', context)  # Renderizar la plantilla para crear un contrato

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
    return render(request, 'victima/lista_beneficiario.html', context)  # Renderizar la plantilla con el contexto

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


# Crear en django una vista  para actualizar un beneficiario de la base de datos
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

#elimiar un beneficiario de la base de datos
def delete_beneficiary(request, beneficiary_id):
    beneficiario = get_object_or_404(Beneficiarios, id=beneficiary_id)  # Obtén el beneficiario de la BD
    if request.method == 'POST':
        beneficiario.delete()  # Eliminar el beneficiario
        return redirect('lista_beneficiarios')  # Redirige después de la eliminación
    return render(request, 'victima/eliminar_beneficiario.html', {'beneficiario': beneficiario})  # Confirmar eliminación

# Crear en django una vista que muestre un listado de entregas
def entregas_list(request):
    entregas= Entregas.objects.all()  # Obtener lista de entregas de la base de datos
    context = {
        'entregas': entregas  # Pasar los entregas al contexto
    }
    return render(request, 'victima_app/lista_entregas.html', context)

#crear una vista en django para crear una entrega

def crear_entregas(request):
    if request.method == 'POST':
        cantidad = request.POST.get('cantidad')
        fecha_entrega = request.POST.get('fecha_entrega')
        contrato = contrato.objects.all()  # Obtener todas las entregas
        contrato_ids = [contrato.id for contrato in contrato]  # Extraer los IDs
        contrato.objects.create(
            cantidad=cantidad,
            fecha_entrega=fecha_entrega,
            id_contrato_id=contrato_ids[0]  # Asignar el primer beneficiario como ejemplo
        )
        return HttpResponseRedirect(reverse("login"))
    return render(request, 'victima_app/crear_entregas.html')  # Renderizar la plantilla para crear un entrega
 
# Crear en django una vista que muestre un listado de entregas
def entregas_list(request):
    entregas= Entregas.objects.all()  # Obtener lista de entregas de la base de datos
    context = {
        'entregas': entregas  # Pasar los entregas al contexto
    }
    return render(request, 'victima_app/lista_entregas.html', context)