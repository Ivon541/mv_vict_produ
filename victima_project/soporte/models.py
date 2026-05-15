from django.db import models

class Ticket(models.Model):

    PRIORIDAD = [
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
        ('critica', 'Crítica'),
    ]

    ESTADO = [
        ('abierto', 'Abierto'),
        ('proceso', 'En proceso'),
        ('resuelto', 'Resuelto'),
    ]

    TIPO = [
        ('consulta', 'Consulta'),
        ('error', 'Error del sistema'),
        ('acceso', 'Problema de acceso'),
        ('otro', 'Otro'),
    ]

    nombre = models.CharField(max_length=100)
    documento = models.CharField(max_length=20)
    correo = models.EmailField()

    tipo = models.CharField(max_length=20, choices=TIPO)
    asunto = models.CharField(max_length=200)
    descripcion = models.TextField()

    prioridad = models.CharField(max_length=10, choices=PRIORIDAD)
    estado = models.CharField(max_length=10, choices=ESTADO, default='abierto')

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_resolucion = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.asunto


class FAQ(models.Model):
    pregunta = models.CharField(max_length=255)
    respuesta = models.TextField()

    def __str__(self):
        return self.pregunta