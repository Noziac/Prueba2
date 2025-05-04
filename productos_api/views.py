from django.shortcuts import render, get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt

from core.models import Version, Skins, Pve, AgrandarAlijo
from .serializers import VersionSerializer, SkinsSerializer, PveSerializer, AgrandarAlijoSerializer

# Create your views here.

@csrf_exempt
@api_view(['GET'])
def lista_productos(request):
    if request.method == 'GET':
        versiones = Version.objects.all()
        versiones_serializer = VersionSerializer(versiones, many=True)

        skins = Skins.objects.all()
        skins_serializer = SkinsSerializer(skins, many=True)

        pve = Pve.objects.all()
        pve_serializer = PveSerializer(pve, many=True)

        stash = AgrandarAlijo.objects.all()
        stash_serializer = AgrandarAlijoSerializer(stash, many=True)

        all_productos_data = versiones_serializer.data + skins_serializer.data + pve_serializer.data + stash_serializer.data

        return Response(all_productos_data)