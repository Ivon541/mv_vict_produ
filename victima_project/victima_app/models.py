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
    id_beneficiario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100,default='nn')
    tipo_documento = models.CharField(max_length=50,default='nn')
    documento_identidad = models.CharField(max_length=20, unique=True,default='nn')
    fecha_nacimiento = models.DateField(default='2000-01-01')
    direccion = models.CharField(max_length=255,default='nn')
    telefono = models.CharField(max_length=15,default='nn')
    email = models.EmailField(default='nn')
    fecha_registro = models.DateField(default='2000-01-01') 
    
    
class Contratos(models.Model):
    ETAPA = {
        'pre': 'Preejecucion',
        'eje': 'Ejecucion',
        'liq': 'Liquidacion',
    }
    id_contrato = models.AutoField(primary_key=True)
    id_beneficiario = models.ForeignKey(Beneficiarios, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    etapa = models.CharField(max_length=20, choices=ETAPA)
    monto = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    fecha_registro = models.DateField(default='2000-01-01')
    tipo_contrato = models.CharField(max_length=50,default='nn')
    objecto = models.TextField(default='nn')
    
    
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








