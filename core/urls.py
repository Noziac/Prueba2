from django.urls import path
from .views import Principal, Comprar, Soporte, Registrar, Ingresar, Versiones, Extensiones, Skins, Stash

# path('', , name=""),

urlpatterns = [
    path('Principal', Principal, name="Principal"),
    path('Comprar', Comprar, name="Comprar"),
    path('Soporte', Soporte, name="Soporte"),
    path('Registrar', Registrar, name="Registrar"),
    path('Ingresar', Ingresar, name="Ingresar"),
    path('Versiones', Versiones, name="Versiones"),
    path('Extensiones', Extensiones, name="Extensiones"),
    path('Skins', Skins, name="Skins"),
    path('Stash', Stash, name="Stash"),
]