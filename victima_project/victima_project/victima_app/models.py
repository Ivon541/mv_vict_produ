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
    documento_identidad = models.CharField(max_length=20, unique=True)
    
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
    
class Productos(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

class Entregas(models.Model):
    id_entrega = models.AutoField(primary_key=True)
    id_contrato = models.ForeignKey(Contratos, on_delete=models.CASCADE)
    id_producto = models.ForeignKey(Productos, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha_entrega = models.DateField()

class Programas(models.Model):
    id_programa = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

class BeneficiarioProgramas(models.Model):  
    id_beneficiario = models.ForeignKey(Beneficiarios,on_delete=models.CASCADE)
    id_programa = models.ForeignKey(Programas, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('id_beneficiario', 'id_programa')




