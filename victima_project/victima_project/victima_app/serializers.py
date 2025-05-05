from rest_framework import serializers
from .models import Usuario, Contratos


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'nombre_usuario', 'contraseña', 'email', 'telefono', 'rol']

class ContratosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contratos
        fields = ['id_contrato', 'id_beneficiario', 'fecha_inicio', 'fecha_fin', 'etapa']