from rest_framework import serializers
from core.models import Version, Skins, Pve, AgrandarAlijo

class VersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Version
        fields = ['id_version', 'activo', 'imagen']

class SkinsSerializer(serializers.ModelSerializer):
    facción_display = serializers.CharField(source='get_facción_display', read_only=True)

    class Meta:
        model = Skins
        fields = ['nombre', 'descripcion', 'precio', 'imagen', 'facción', 'facción_display']

class PveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pve
        fields = ['nombre', 'descripcion', 'precio']

class AgrandarAlijoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgrandarAlijo
        fields = ['nombre', 'descripcion', 'precio', 'imagen']
