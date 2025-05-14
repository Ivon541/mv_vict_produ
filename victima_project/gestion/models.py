from django.db import models
from django.contrib.auth.models import User

class Turno(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    hora_ingreso = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=[
        ('en_espera', 'En Espera'),
        ('atendido', 'Atendido')
    ], default='en_espera')

    def __str__(self):
        return f"Turno de {self.usuario.username} - {self.estado}"

class HistorialAccion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    accion = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} hizo: {self.accion} en {self.fecha}"