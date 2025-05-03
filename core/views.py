import requests
import os
import random
from dotenv import load_dotenv
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .models import Version, Skins, Pve, AgrandarAlijo, PerfilUsuario, Ticket, Version
from django.templatetags.static import static
from django.urls import reverse
from django.contrib import messages
from .forms import EditarPerfilForm, EditarAvatarForm
from django.db import IntegrityError
from django.contrib.auth.models import User
from .forms import CrearTicketForm


load_dotenv()

def Principal(request):
    return render(request, 'core/principal.html')

@login_required
def Comprar(request):
    versiones_lista = Version.objects.filter(activo=True).order_by('-precio')
    return render(request, 'core/productos/versiones.html', {'versiones': versiones_lista})

@login_required
def Soporte(request):
    return render(request, 'core/soporte.html')

@login_required
def CTickets(request):
    if request.method == 'POST':
        form = CrearTicketForm(request.POST)
        if form.is_valid():
            nuevo_ticket = form.save(commit=False)
            nuevo_ticket.usuario = request.user
            nuevo_ticket.save()
            messages.success(request, 'Ticket creado exitosamente. Te responderemos a la brevedad.')
            return redirect('MTickets')  # Redirige a la lista de tickets
    else:
        form = CrearTicketForm()
    return render(request, 'core/crear_tickets.html', {'form': form})

@login_required
def MTickets(request):
    tickets = Ticket.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    return render(request, 'core/mis_tickets.html', {'tickets': tickets})

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

    if request.method == 'POST':
        version_id = request.POST.get('version_id')
        if version_id:
            try:
                version = get_object_or_404(Version, pk=version_id, activo=True)
                compra_realizada = request.session.get(f'comprado_version_{version_id}', False)

                if compra_realizada:
                    messages.warning(request, f'Ya compraste la versión "{version.nombre}".')
                else:
                    Compra.objects.create(usuario=request.user, version=version)
                    messages.success(request, f'¡Compra exitosa de la versión "{version.nombre}"!')
                    request.session[f'comprado_version_{version_id}'] = True
                    # Redirigir a una página GET (la página de éxito)
                    return redirect('exito')
            except Version.DoesNotExist:
                messages.error(request, 'La versión seleccionada no existe.')
        else:
            messages.error(request, 'No se especificó la versión a comprar.')

    return render(request, 'core/productos/versiones.html', {'versiones': versiones_lista})

def exito(request):
    mensaje = "¡Compra exitosa! Gracias por tu compra."
    return render(request, 'core/exito.html', {'mensaje': mensaje})

def exito(request):
    mensaje = "¡Compra exitosa! Gracias por tu compra."
    return render(request, 'core/exito.html', {'mensaje': mensaje})


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


def Stash(request):
    return render(request, 'core/productos/stash.html')
