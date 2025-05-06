from django.shortcuts import render, get_object_or_404
from rest_framework import status

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Resena
from .serializers import ResenaSerializer

# Create your views here.

@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def lista_resenas(request):
    if request.method == 'GET':
        resenas = Resena.objects.all()
        serilizer = ResenaSerializer(resenas, many=True)

        return Response(serilizer.data)
    
@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def vista_resenas(request, id):
    try:
        resena = Resena.objects.get(id=id)
    except Resena.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = ResenaSerializer(resena)
        return Response(serializer.data)