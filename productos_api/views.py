from django.shortcuts import render, get_object_or_404
from rest_framework import status

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

# LISTAS
@csrf_exempt
@api_view(['GET'])
def lista_versiones(request):
    if request.method == 'GET':
        versiones = Version.objects.all()
        serializer = VersionSerializer(versiones, many=True)
        
        return Response(serializer.data)

@csrf_exempt
@api_view(['GET'])
def lista_skins(request):
    if request.method == 'GET':
        skins = Skins.objects.all()
        serializer = SkinsSerializer(skins, many=True)
        
        return Response(serializer.data)

@csrf_exempt
@api_view(['GET'])
def lista_pve(request):
    if request.method == 'GET':
        pve = Pve.objects.all()
        serializer = PveSerializer(pve, many=True)
        
        return Response(serializer.data)

@csrf_exempt
@api_view(['GET'])
def lista_alijos(request):
    if request.method == 'GET':
        alijos = AgrandarAlijo.objects.all()
        serializer = AgrandarAlijoSerializer(alijos, many=True)
        
        return Response(serializer.data)
    
# VISTAS
@csrf_exempt
@api_view(['GET'])
def vista_versiones(request, id):
    try:
        versiones = Version.objects.get(id=id)
    except Version.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = VersionSerializer(versiones)
        return Response(serializer.data)
    
@csrf_exempt
@api_view(['GET'])
def vista_skins(request, id):
    try:
        skins = Skins.objects.get(id=id)
    except Skins.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = SkinsSerializer(skins)
        return Response(serializer.data)
    
@csrf_exempt
@api_view(['GET'])
def vista_pve(request, id):
    try:
        pve = Pve.objects.get(id=id)
    except Pve.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = PveSerializer(pve)
        return Response(serializer.data)
    
@csrf_exempt
@api_view(['GET'])
def vista_alijos(request, id):
    try:
        alijo = AgrandarAlijo.objects.get(id=id)
    except AgrandarAlijo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = AgrandarAlijoSerializer(alijo)
        return Response(serializer.data)