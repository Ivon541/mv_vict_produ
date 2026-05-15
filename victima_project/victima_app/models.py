from django.db import models

# Create your models here.
class Usuario(models.Model):
    ROL = {
        'A':'Administrador',
        'C': 'Consultor',
    }
    id_usuario = models.AutoField(primary_key=True)
    nombre_usuario = models.CharField(max_length=50)
    contraseña = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15)
    rol = models.CharField(max_length=20, choices=ROL)
    
class Beneficiarios(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('procesado', 'Procesado'),
    ]
    id_beneficiario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100,default='nn')
    tipo_documento = models.CharField(max_length=50,default='nn')
    documento_identidad = models.CharField(max_length=20, unique=True,default='nn')
    fecha_nacimiento = models.DateField(default='2000-01-01')
    direccion = models.CharField(max_length=255,default='nn')
    telefono = models.CharField(max_length=15,default='nn')
    email = models.EmailField(default='nn')
    fecha_registro = models.DateField(auto_now_add=True) 
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')

    class Meta:
        ordering = ['fecha_registro']  # El ultimo registro ingresado es el primero en la lista (FIFO - COLA)
    
    
class Contratos(models.Model):
    ETAPA_CHOICES = [
        ('pre', 'Preejecucion'),
        ('eje', 'Ejecucion'),
        ('liq', 'Liquidacion'),
    ]
    id_contrato = models.AutoField(primary_key=True)
    id_beneficiario = models.ForeignKey(Beneficiarios, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    etapa = models.CharField(max_length=20, choices=ETAPA_CHOICES)
    monto = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    fecha_registro = models.DateField(auto_now_add=True)
    tipo_contrato = models.CharField(max_length=50,default='nn')
    objecto = models.TextField(default='nn')

    class Meta:
        ordering = ['-fecha_registro']  # Ultimo contrato agregado es el ultimo en la lista (LIFO -PILA)
    
    
class Productos(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    cantidad = models.IntegerField(default=0)
    fecha_entrada = models.DateField(default='2000-01-01')
    fecha_salida = models.DateField(default='2000-01-01')
    

class Entregas(models.Model):
    id_entrega = models.AutoField(primary_key=True)
    id_contrato = models.ForeignKey(Contratos, on_delete=models.CASCADE)
    id_producto = models.ForeignKey(Productos, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha_entrega = models.DateField()

class Programas(models.Model):
    id_programa = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    tipo_programa = models.CharField(max_length=50,default='nn')
    fecha_inicio = models.DateField(default='2000-01-01')
    fecha_finalizacion = models.DateField(default='2000-01-01')
    descripcion = models.TextField(default='nn')

class BeneficiarioProgramas(models.Model):  
    id_beneficiario = models.ForeignKey(Beneficiarios,on_delete=models.CASCADE)
    id_programa = models.ForeignKey(Programas, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('id_beneficiario', 'id_programa')

from .models import Beneficiarios, BeneficiarioProgramas, Programas

def consultar_programa(request):
    programas = None
    ciudadano = None
    documento_identidad = request.GET.get('documento_identidad', '').strip()

    if documento_identidad:
        try:
            ciudadano = Beneficiarios.objects.get(documento_identidad=documento_identidad)
            # Obtener los programas asociados al beneficiario
            beneficiario_programas = BeneficiarioProgramas.objects.filter(
                id_beneficiario=ciudadano
            ).select_related('id_programa')
            
            programas = [bp.id_programa for bp in beneficiario_programas]
            
        except Beneficiarios.DoesNotExist:
            programas = []  # Vacío pero no None → activa el mensaje "no encontrado"

    return render(request, 'aut_app/home.html', {
        'programas': programas,
        'ciudadanos': ciudadano,
        'documento_identidad': documento_identidad,
    })

def asignar_programa(request):
    beneficiario = None
    programas_asignados = []
    ids_asignados = []
    todos_los_programas = Programas.objects.all()
    documento_identidad = ''
    mensaje = ''

    # GET → buscar beneficiario
    if request.method == 'GET':
        documento_identidad = request.GET.get('documento_identidad', '').strip()
        if documento_identidad:
            try:
                beneficiario = Beneficiarios.objects.get(documento_identidad=documento_identidad)
                relaciones = BeneficiarioProgramas.objects.filter(
                    id_beneficiario=beneficiario
                ).select_related('id_programa')
                programas_asignados = [r.id_programa for r in relaciones]
                ids_asignados = [p.id_programa for p in programas_asignados]
            except Beneficiarios.DoesNotExist:
                beneficiario = None

    # POST → asignar programa
    elif request.method == 'POST':
        id_beneficiario = request.POST.get('id_beneficiario')
        id_programa = request.POST.get('id_programa')
        documento_identidad = request.POST.get('documento_identidad', '')

        beneficiario = get_object_or_404(Beneficiarios, id_beneficiario=id_beneficiario)
        programa = get_object_or_404(Programas, id_programa=id_programa)

        _, creado = BeneficiarioProgramas.objects.get_or_create(
            id_beneficiario=beneficiario,
            id_programa=programa
        )

        mensaje = f"✅ Programa '{programa.nombre}' asignado correctamente." if creado else "⚠️ Este programa ya estaba asignado."

        # Recargar programas asignados
        relaciones = BeneficiarioProgramas.objects.filter(
            id_beneficiario=beneficiario
        ).select_related('id_programa')
        programas_asignados = [r.id_programa for r in relaciones]
        ids_asignados = [p.id_programa for p in programas_asignados]
        todos_los_programas = Programas.objects.all()

    return render(request, 'aut_app/asignar_programa.html', {
        'beneficiario': beneficiario,
        'programas_asignados': programas_asignados,
        'ids_asignados': ids_asignados,
        'todos_los_programas': todos_los_programas,
        'documento_identidad': documento_identidad,
        'mensaje': mensaje,
    })




