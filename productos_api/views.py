from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt

from core.models import Version, Skins
from .serializers import VersionSerializer, SkinsSerializer

# Create your views here.

@csrf_exempt
@api_view(['GET'])
def lista_productos(request):
    if request.method == 'GET':
        version = Version.objects.all()
        serializer = VersionSerializer(version, many=True)
        skins = Skins.objects.all()
        serializer = SkinsSerializer(skins, many=True)

        return Response(serializer.data)