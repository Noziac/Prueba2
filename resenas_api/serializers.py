from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from core.models import Resena, Version, Skins, Pve, AgrandarAlijo

class ResenaSerializer(serializers.ModelSerializer):
    nombre_producto = serializers.SerializerMethodField()
    
    class Meta:
        model = Resena
        fields = ['id', 'usuario', 'nombre_producto', 'texto', 'evaluacion', 'fecha_creacion']

    def get_nombre_producto(self, instance):
        try:
            content_type = ContentType.objects.get_for_id(instance.content_type_id)
            model_class = content_type.model_class()

            if model_class == Version:
                producto = get_object_or_404(Version, pk=instance.object_id)
                return producto.nombre
            elif model_class == Skins:
                producto = get_object_or_404(Skins, pk=instance.object_id)
                return producto.nombre
            elif model_class == Pve:
                producto = get_object_or_404(Pve, pk=instance.object_id)
                return producto.nombre
            elif model_class == AgrandarAlijo:
                producto = get_object_or_404(AgrandarAlijo, pk=instance.object_id)
                return producto.nombre
            return None
        except ContentType.DoesNotExist:
            return None
        except (Version.DoesNotExist, Skins.DoesNotExist, Pve.DoesNotExist, AgrandarAlijo.DoesNotExist):
            return None