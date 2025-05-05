from rest_framework import serializers
from core.models import Resena

class ResenaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resena
        fields = ['usuario', 'texto', 'evaluacion', 'fecha_creacion']