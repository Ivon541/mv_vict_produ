from django.shortcuts import render, redirect
from victima_app.models import Contratos, Usuario
from victima_app.models import Beneficiarios, BeneficiarioProgramas
from victima_app.models import Entregas, Programas, Productos
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets
from .serializers import UsuarioSerializer, ContratosSerializer
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.db import connection #from .forms import BeneficiarioForm 
#from .forms import BeneficiarioForm

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

# class BeneficiariosViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = Beneficiarios.objects.all()
#     serializer_class = BeneficiariosSerializer
#     permission_classes = [permissions.IsAuthenticated]


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
        contratos = Contratos.objects.create(
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            etapa=etapa,
            id_beneficiario_id=beneficiarios_ids[0]  # Asignar el primer beneficiario como ejemplo
        )
        context = {
            'contratos': contratos  # Pasar los contratos al contexto
        }
        return HttpResponseRedirect(reverse("contrato_list"), context)  # Redirigir a la lista de contratos después de crear uno
    context = {
        'beneficiarios': beneficiarios  # Pasar los beneficiarios al contexto
    }
    if request.user.is_authenticated:
        return render(request, 'victima_app/crear_contratos.html', context)  # Renderizar la plantilla para crear un contrato
    else:
        return HttpResponseRedirect(reverse("login"))


    


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


def crear_beneficiario(request):
    beneficiarios = Beneficiarios.objects.all()  # Obtener todos los beneficiarios
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        documento_identidad = request.POST.get('documento_identidad')
        tipo_documento = request.POST.get('tipo_documento')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        direccion = request.POST.get('direccion')
        telefono = request.POST.get('telefono')
        email = request.POST.get('email')
        fecha_registro = request.POST.get('fecha_registro')
        
        beneficiario = Beneficiarios.objects.create(
            nombre=nombre,
            apellido=apellido,
            tipo_documento=tipo_documento,
            documento_identidad=documento_identidad,
            fecha_nacimiento=fecha_nacimiento,
            direccion=direccion,    
            telefono=telefono,
            email=email,
            fecha_registro=fecha_registro,
        )
        context = {
            'beneficiarios': beneficiario  # Pasar los beneficiarios al contexto
        }
        return HttpResponseRedirect(reverse("lista_beneficiarios"), context)  # Redirigir a la lista de beneficiarios después de crear uno
        context = {
        'beneficiarios': beneficiarios  # Pasar los beneficiarios al contexto
    }
    return render(request, 'victima_app/crear_beneficiario.html')  # Renderizar la plantilla para crear un beneficiario

# Crear en django una vista que muestre un listado de   beneficiarios
def beneficiary_list(request):
    beneficiarios = Beneficiarios.objects.all()
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        documento_identidad = request.POST.get('documento_identidad')
        email = request.POST.get('email')
       
        
        Beneficiarios.objects.create(
            nombre=nombre,
            apellido=apellido,
            documento_identidad=documento_identidad,
            email=email,
           
        )
        return HttpResponseRedirect(reverse("lista_beneficiarios"))  # Redirigir a la lista de beneficiarios después de crear uno
    
    context = {
        'beneficiarios': beneficiarios  # Pasar los beneficiarios al contexto
    }
    return render(request,'victima_app/lista_beneficiarios.html', context) # Renderizar la plantilla con el contexto


# Crear en django una vista  para actualizar un beneficiario de la base de datos
# def update_beneficiary(request, beneficiary_id):
#     beneficiario = get_object_or_404(Beneficiario, id=beneficiary_id)  # Obtén el beneficiario de la BD

#     if request.method == 'POST':
#         form = BeneficiarioForm(request.POST, instance=beneficiario)  # Cargar datos en el formulario
#         if form.is_valid():
#             form.save()
#             return redirect('lista_beneficiarios')  # Redirige después de la actualización
#     else:
#         form = BeneficiarioForm(instance=beneficiario)  # Mostrar datos actuales en el formulario

#     return render(request, 'victima/actualizar_beneficiario.html', {'form': form, 'beneficiario': beneficiario}) # Renderizar la plantilla para actualizar un beneficiario

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
    return render(request, 'victima_app/crear_beneficiario.html', {'beneficiarios': beneficiarios})

#elimiar un beneficiario de la base de datos
def eliminar_beneficiario(request, id_beneficiario):
    beneficiario = Beneficiarios.objects.get(pk=id_beneficiario)  # Obtener el beneficiario por ID

    if request.method == 'POST':
        beneficiario.delete()  # Eliminar el beneficiario de la base de datos
        return redirect('lista_beneficiarios')  # Redirigir a la lista de beneficiarios

    context = {
        'beneficiario': beneficiario  # Pasar el beneficiario al contexto
    }
    return render(request, 'victima_app/eliminar_beneficiario.html', context)  # Renderizar la plantilla para confirmar la eliminación
      
def editar_beneficiario(request, id_beneficiario):
    beneficiario = Beneficiarios.objects.get(pk=id_beneficiario)  # Obtener el beneficiario por ID

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        documento_identidad = request.POST.get('documento_identidad')
        tipo_documento = request.POST.get('tipo_documento')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        direccion = request.POST.get('direccion')
        telefono = request.POST.get('telefono')
        email = request.POST.get('email')
        return redirect("lista_beneficiarios")  # Redirigir a la lista de contratos

    context = {
        'beneficiario': beneficiario # Pasar el contrato al contexto
    }
    return render(request, 'victima_app/editar_beneficiario.html', context) 

#crear una vista en django para crear un programa
def crear_programa(request):
    programa = Programas.objects.all()
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        tipo_programa = request.POST.get('tipo_programa')
        descripcion = request.POST.get('descripcion')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_finalizacion = request.POST.get('fecha_fin')
        
        Programas.objects.create(
            nombre=nombre,
            tipo_programa=tipo_programa,
            descripcion=descripcion,
            fecha_inicio=fecha_inicio,
            fecha_finalizacion=fecha_finalizacion,
        )
        return HttpResponseRedirect(reverse('lista_programas'))
        context = {
        'programa': programa # Pasar los beneficiarios al contexto
    }   
    return render(request, 'victima_app/crear_programas.html')  # Renderizar la plantilla para crear un programa

# Crear en django una vista que muestre un listado de programas
def lista_programas(request):
    programa = Programas.objects.all()  # Obtener lista de programas de la base de datos
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        tipo_programa = request.POST.get('tipo_programa')
        
        Programas.objects.create(
            nombre=nombre,
            tipo_programa = request.POST.get('tipo_programa')
           
        )
        return HttpResponseRedirect(reverse("crear-programas"))  # Redirigir a la lista de beneficiarios después de crear uno
        context = {
        'programas': programa  # Pasar los beneficiarios al contexto
    }
        
    context = {
        'programas': programa  # Pasar los beneficiarios al contexto
    }
    return render(request,'victima_app/lista_programas.html', context) # Renderizar la plantilla con el contexto

 
def editar_programa(request, id_programa):
    programa = Programas.objects.get(pk=id_programa)  # Obtener el programa por ID

    if request.method == 'POST':
        programa.nombre = request.POST.get('fecha_inicio')
        programa.fecha_inicio = request.POST.get('fecha_fin')
        programa.etapa = request.POST.get('etapa')
        return redirect('lista_programas')  # Redirigir a la lista de programa

    context = {
        'programas': programa  # Pasar el programa al contexto
    }
    return render(request, 'victima_app/editar_programa.html', context)  # Renderizar la plantilla para editar un contrato


def eliminar_programa(request, id_programa):
    programa = Programas.objects.get(pk=id_programa)  # Obtener el contrato por ID

    if request.method == 'POST':
        programa.delete()  # Eliminar el contrato de la base de datos
        return redirect('programa_list')  # Redirigir a la lista de contratos

    context = {
        'Programas': Programas  # Pasar el contrato al contexto
    }
    return render(request, 'victima_app/eliminar_programa.html', context)  # Renderizar la plantilla para confirmar la eliminación


def crear_entrega(request):
    entrega = Entregas.objects.all()
    if request.method == 'POST':
        id_contrato = request.POST.get('id_contrato')
        id_producto = request.POST.get('id_producto')
        cantidad = request.POST.get('cantidad')
        fecha_entrega = request.POST.get('fecha_entrega')
        
        
        Entregas.objects.create(
            id_contrato=id_contrato,
            id_producto=id_producto,
            cantidad=cantidad,
            fecha_entrega=fecha_entrega,
        )
        return HttpResponseRedirect(reverse('lista_entregas'))
        context = {
        'entrega': entrega # Pasar los beneficiarios al contexto
    }   
    return render(request, 'victima_app/crear_entregas.html')  # Renderizar la plantilla para crear un programa

# Crear en django una vista que muestre un listado de programas
def lista_entregas(request):
    entrega = Entregas.objects.all()  # Obtener lista de programas de la base de datos
    if request.method == 'POST':
        id_contrato = request.POST.get('id_contrato')
        id_producto = request.POST.get('id_producto')
        cantidad = request.POST.get('cantidad')
        fecha_entrega = request.POST.get('fecha_entrega')
        
        Entregas.objects.create(
            id_contrato=id_contrato,
            id_producto=id_producto,
            cantidad=cantidad,
            fecha_entrega=fecha_entrega,
           
        )
        return HttpResponseRedirect(reverse("crear-entregas"))  # Redirigir a la lista de beneficiarios después de crear uno
        context = {
        'entregas': entrega  # Pasar los beneficiarios al contexto
    }
        
    context = {
        'entregas': entrega  # Pasar los beneficiarios al contexto
    }
    return render(request,'victima_app/lista_entregas.html', context) # Renderizar la plantilla con el contexto

 
def editar_entrega(request, id_entrega):
    entrega = Entregas.objects.get(pk=id_entrega)  # Obtener el programa por ID

    if request.method == 'POST':
        entrega.nombre = request.POST.get('fecha_inicio')
        entrega.fecha_inicio = request.POST.get('fecha_fin')
        entrega.etapa = request.POST.get('etapa')
        return redirect('lista_entregas')  # Redirigir a la lista de programa

    context = {
        'entregas': entregas  # Pasar el programa al contexto
    }
    return render(request, 'victima_app/editar_entrega.html', context)  # Renderizar la plantilla para editar un contrato


def eliminar_entrega(request, id_entrega):
    entrega = Entregas.objects.get(pk=id_entrega)  # Obtener el contrato por ID

    if request.method == 'POST':
        entrega.delete()  # Eliminar el contrato de la base de datos
        return redirect('entrega_list')  # Redirigir a la lista de contratos

    context = {
        'Entregas': Entregas  # Pasar el contrato al contexto
    }
    return render(request, 'victima_app/eliminar_entrega.html', context)  # Renderizar la plantilla para confirmar la eliminación

#crear una vista en django para crear un producto de la base de datos del proyecto victima
def crear_producto(request):
    producto = Productos.objects.all()
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        cantidad = request.POST.get('cantidad')
        fecha_registro = request.POST.get('fecha_registro')
        
        Productos.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            cantidad=cantidad,
            fecha_registro=fecha_registro,
        )
        return HttpResponseRedirect(reverse('lista_productos'))
        context = {
        'producto': producto # Pasar los beneficiarios al contexto
    }   
    return render(request, 'victima_app/crear_productos.html')  # Renderizar la plantilla para crear un programa

def consultar_programa(request):
    documento_identidad = request.GET.get('documento_identidad')  # Obtener el documento de identidad desde el parámetro GET
    programas = Programas.objects.none()  # Inicializar con un queryset vacío

    if documento_identidad:
        beneficiarios = Beneficiarios.objects.filter(documento_identidad=documento_identidad)  # Buscar beneficiarios por documento
        
        if beneficiarios.exists():            
            beneficiario_ids = beneficiarios.values_list('id_beneficiario', flat=True)  # Obtener los IDs de los beneficiarios            
            beneficiario_programas_ids = BeneficiarioProgramas.objects.filter(id_beneficiario__in=beneficiario_ids).values_list('id_programa', flat=True)  # Obtener los IDs de los programas relacionados
            programas = Programas.objects.filter(id_programa__in=beneficiario_programas_ids)  # Filtrar programas relacionados

    
    if Beneficiarios.objects.filter(documento_identidad=documento_identidad).exists():  # Obtener todos los beneficiarios
        ciudadanos = Beneficiarios.objects.get(documento_identidad=documento_identidad)
    else:  # Obtener todos los beneficiarios:
        ciudadanos = ""

    context = {
        'programas': programas,  # Pasar los programas al contexto
        'documento_identidad': documento_identidad, # Pasar el documento de identidad al contexto
        'ciudadanos': ciudadanos,  # Pasar los beneficiarios al contexto
    }
    return render(request, 'aut_app/home.html', context)  # Renderizar la plantilla con el contexto

def asignar_programa(request):
    beneficiarios = Beneficiarios.objects.all()  # Obtener todos los beneficiarios
    if request.method == 'POST':
        id_beneficiario = request.POST.get('id_beneficiario')  # Obtener el ID del beneficiario seleccionado
        return HttpResponseRedirect(reverse('detalle_beneficiario', args=[id_beneficiario]))  # Redirigir al detalle del beneficiario

    context = {
        'beneficiarios': beneficiarios  # Pasar los beneficiarios al contexto
    }
    return render(request, 'victima_app/asignar_programa.html', context)  # Renderizar la plantilla con el contexto