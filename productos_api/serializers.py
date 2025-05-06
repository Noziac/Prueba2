from rest_framework import serializers
from core.models import Version, Skins, Pve, AgrandarAlijo

class VersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Version
        fields = ['id_version', 'nombre', 'descripcion', 'precio', 'activo', 'imagen']

class SkinsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skins
        fields = ['id', 'nombre', 'descripcion', 'precio', 'imagen', 'facción']

class PveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pve
        fields = ['id', 'nombre', 'descripcion', 'precio']

class AgrandarAlijoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgrandarAlijo
        fields = ['id', 'nombre', 'descripcion', 'precio', 'imagen']
