from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Version, Skins, Pve, AgrandarAlijo
from django.templatetags.static import static
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

def Principal(request):
    return render(request, 'core/principal.html')

def Comprar(request):
    return render(request, 'core/comprar.html')

@login_required
def Soporte(request):
    return render(request, 'core/soporte.html')

@login_required
def CTickets(request):
    return render(request, 'core/crear_tickets.html')

@login_required
def MTickets(request):
    return render(request, 'core/mis_tickets.html')

@login_required
def Perfil(request):
    return render(request, 'core/perfil.html')

def Registrar(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('Principal')
        else:
            return render(request, 'core/registrar.html', {'form': form})
    else:
        form = UserCreationForm()
        return render(request, 'core/registrar.html', {'form': form})
    
def Ingresar(request):
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        clave = request.POST.get('pass')

        print(f"Intentando iniciar sesión con el usuario: '{usuario}'")
        user = authenticate(request, username=usuario, password=clave)
        print(f"Resultado de authenticate: {user}")

        if user is not None:
            login(request, user)
            print("Redirigiendo a Principal")
            return redirect('Principal')
        else:
            context = {
                'error': 'Error, intente nuevamente.'
            }
            print(f"Error de autenticación: {context['error']}")
            return render(request, 'core/Ingresar.html', context)
    return render(request, 'core/Ingresar.html')

def Recuperar(request):
    return render(request, 'core/recuperar.html')

def Versiones(request):
    versiones_lista = Version.objects.filter(activo=True).order_by('-precio')
    return render(request, 'core/productos/versiones.html', {'versiones': versiones_lista})

def Extensiones(request, categoria=None):
    if categoria == 'skins':
        usec_skins = Skins.objects.filter(facción='usec')
        bear_skins = Skins.objects.filter(facción='bear')
        return render(request, 'core/productos/skins.html', {
            'bear_skins': bear_skins,
            'usec_skins': usec_skins,
        })
    elif categoria == 'comprar_pve':
        if request.method == 'POST':
            mensaje = "¡Compra de PvE realizada con éxito!"
            return render(request, 'core/productos/exito.html', {'mensaje': mensaje})
        else:
            return redirect('extensiones')
    elif categoria == 'stash':
        alijos = AgrandarAlijo.objects.all()
        return render(request, 'core/productos/stash.html', {'alijos': alijos})
    else:
        skin_representativo = Skins.objects.first()
        pve_representativo = Pve.objects.first()
        alijo_representativo = AgrandarAlijo.objects.first()

        return render(request, 'core/productos/extensiones.html', {
            'skin_imagen': static('img/skins.png'),
            'skin_descripcion': "Accede a una variedad de opciones de personalización visual para tu personaje. Adapta tu estilo en el juego con atuendos únicos y accesorios, reflejando tu personalidad o estrategias tácticas.",
            'pve_imagen': static('img/pve.png'),
            'pve_descripcion':  "Explora nuevos desafíos en el entorno jugador contra entorno. Enfréntate a enemigos controlados por inteligencia artificial y perfecciona tus habilidades en un entorno más controlado, sin la presión del combate jugador contra jugador.",
            'alijo_imagen': static('img/stash.png'),
            'alijo_descripcion': "Amplía significativamente tu espacio de almacenamiento, proporcionando un inventario más grande para gestionar objetos valiosos y recursos esenciales. Esto te permitirá acumular más equipo sin preocuparte por el límite de espacio.",
            'pve_url_compra': reverse('extensiones_categoria', kwargs={'categoria': 'comprar_pve'}),
        })

@login_required
def Stash(request):
    return render(request, 'core/productos/stash.html')