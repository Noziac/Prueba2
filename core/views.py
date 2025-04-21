import requests
import os
import random
from dotenv import load_dotenv
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Version, Skins, Pve, AgrandarAlijo, PerfilUsuario
from django.templatetags.static import static
from django.urls import reverse
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .forms import EditarPerfilForm, EditarAvatarForm
from django.contrib.auth import update_session_auth_hash
from django.db import IntegrityError
from django.contrib.auth.models import User

load_dotenv()

def Principal(request):
    tarkov_streamers_usernames = ['pestily', 'lvndmark', 'baxbeast', 'drlupo', 'willerz']
    all_streamers_data = obtener_info_twitch(request, tarkov_streamers_usernames)

    live_tarkov_streamers = [s for s in all_streamers_data if s['is_live']]
    random_live_streamer = random.choice(live_tarkov_streamers) if live_tarkov_streamers else None

    context = {
        'random_streamer': random_live_streamer,
        'all_streamers': all_streamers_data,
    }
    return render(request, 'core/principal.html', context)

def Comprar(request):
    versiones_lista = Version.objects.filter(activo=True).order_by('-precio')
    return render(request, 'core/productos/versiones.html', {'versiones': versiones_lista})

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
    if not request.user.is_authenticated:
        return redirect('Ingresar')

    info_form = EditarPerfilForm(instance=request.user)
    password_form = PasswordChangeForm(request.user)
    avatar_form = EditarAvatarForm(instance=request.user.perfilusuario)

    if request.method == 'POST':
        if 'actualizar_info' in request.POST:
            info_form = EditarPerfilForm(request.POST, instance=request.user)
            if info_form.is_valid():
                request.user.username = info_form.cleaned_data['username']
                request.user.first_name = info_form.cleaned_data['first_name']
                request.user.last_name = info_form.cleaned_data['last_name']
                request.user.email = info_form.cleaned_data['email']
                request.user.save()
                messages.success(request, 'Tu perfil ha sido actualizado.')
                return redirect('Perfil')
        elif 'cambiar_password' in request.POST:
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Tu contraseña ha sido cambiada exitosamente.')
                return redirect('Perfil')
            else:
                messages.error(request, 'Por favor, corrige los errores en el formulario de contraseña.')

    context = {
        'form_info': info_form,
        'form_password': password_form,
        'form_avatar': avatar_form,
    }
    return render(request, 'core/perfil.html', context)

def Registrar(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        errores = {}

        if not username:
            errores['username'] = 'El nombre de usuario es obligatorio.'
        elif User.objects.filter(username=username).exists():
            errores['username'] = 'Este nombre de usuario ya está en uso.'

        if not email:
            errores['email'] = 'El correo electrónico es obligatorio.'
        elif User.objects.filter(email=email).exists():
            errores['email'] = 'Esta dirección de correo electrónico ya está registrada.'
        elif '@' not in email or '.' not in email:
            errores['email'] = 'Por favor, introduce un correo electrónico válido.'

        if not password:
            errores['password'] = 'La contraseña es obligatoria.'
        elif password != password2:
            errores['password2'] = 'Las contraseñas no coinciden.'

        if errores:
            return render(request, 'core/registrar.html', {'errores': errores, 'username': username, 'email': email})
        else:
            try:
                user = User.objects.create_user(username=username, email=email, password=password)
                PerfilUsuario.objects.create(usuario=user)
                login(request, user)
                return redirect('Principal')
            except IntegrityError as e:
                if 'unique constraint' in str(e).lower():
                    if 'username' in str(e).lower():
                        errores['username'] = 'Este nombre de usuario ya está en uso.'
                    elif 'email' in str(e).lower():
                        errores['email'] = 'Esta dirección de correo electrónico ya está registrada.'
                    else:
                        errores['db_error'] = 'Ocurrió un error al registrar el usuario (unicidad violada).'
                else:
                    errores['db_error'] = f'Ocurrió un error en la base de datos: {e}'
                return render(request, 'core/registrar.html', {'errores': errores, 'username': username, 'email': email})
    else:
        return render(request, 'core/registrar.html')

    
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


# TWITCH TWITCH TWITCH TWITCH TWITCH TWITCH TWITCH TWITCH TWITCH TWITCH TWITCH TWITCH TWITCH TWITCH TWITCH TWITCH TWITCH TWITCH 
def obtener_info_twitch(request, usernames):
    client_id = os.environ.get('TWITCH_CLIENT_ID')
    client_secret = os.environ.get('TWITCH_CLIENT_SECRET')

    if not client_id or not client_secret:
        print("¡ERROR! No se encontraron las variables de entorno de Twitch.")
        return []

    auth_params = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials'
    }
    auth_url = 'https://id.twitch.tv/oauth2/token'
    auth_response = requests.post(auth_url, params=auth_params)
    auth_response.raise_for_status()
    access_token = auth_response.json().get('access_token')

    if not access_token:
        print("¡ERROR! No se pudo obtener el token de acceso de Twitch.")
        return []

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Client-Id': client_id
    }

    streamer_info = []
    for username in usernames:
        user_url = f'https://api.twitch.tv/helix/users?login={username}'
        user_response = requests.get(user_url, headers=headers)
        user_response.raise_for_status()
        user_data = user_response.json().get('data')
        user_id = user_data[0].get('id') if user_data else None

        if user_id:
            stream_url = f'https://api.twitch.tv/helix/streams?user_id={user_id}'
            stream_response = requests.get(stream_url, headers=headers)
            stream_response.raise_for_status()
            stream_data = stream_response.json().get('data')
            is_live = len(stream_data) > 0
            stream_info = stream_data[0] if is_live else None

            streamer_info.append({
                'username': username,
                'is_live': is_live,
                'stream_info': stream_info,
                'user_info': user_data[0] if user_data else None
            })
        else:
            streamer_info.append({
                'username': username,
                'is_live': False,
                'stream_info': None,
                'user_info': None
            })

    return streamer_info