from django.shortcuts import render

# def (request):
#     return render(request, 'core/.html')

# Create your views here.
def Principal(request):
    return render(request, 'core/principal.html')

def Comprar(request):
    return render(request, 'core/comprar.html')

def Soporte(request):
    return render(request, 'core/soporte.html')

def CTickets(request):
    return render(request, 'core/crear_tickets.html')

def MTickets(request):
    return render(request, 'core/mis_tickets.html')

def Registrar(request):
    return render(request, 'core/registrar.html')

def Ingresar(request):
    return render(request, 'core/ingresar.html')

def Versiones(request):
    return render(request, 'core/versiones.html')

def Extensiones(request):
    return render(request, 'core/extensiones.html')

def Skins(request):
    return render(request, 'core/skins.html')

def Stash(request):
    return render(request, 'core/stash.html')
