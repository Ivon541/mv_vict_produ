from rest_framework import serializers
from .models import Beneficiarios, Programas

class ProgramaSerializer(serializers.ModelSerializer):
    class __all__:
        model = Programas
        fields = ['nombre', 'tipo_programa', 'descripcion']

class ConsultaCiudadanoSerializer(serializers.ModelSerializer):
    # Relacionamos los programas asignados
    programas = serializers.SerializerMethodField()

    class Meta:
        model = Beneficiarios
        fields = ['nombre', 'apellido', 'documento_identidad', 'programas']

    def get_programas(self, obj):
        # Buscamos los programas a través de la tabla intermedia
        relaciones = BeneficiarioProgramas.objects.filter(id_beneficiario=obj)
        return ProgramaSerializer([r.id_programa for r in relaciones], many=True).data