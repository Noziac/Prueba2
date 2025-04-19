from django.urls import path
from .views import Principal, Comprar, Soporte, CTickets, MTickets, Registrar, Ingresar, Versiones, Extensiones, Skins, Stash

# path('', , name=""),

urlpatterns = [
    path('Principal', Principal, name="Principal"),
    path('Comprar', Comprar, name="Comprar"),
    path('Soporte', Soporte, name="Soporte"),
    path('CTickets', CTickets, name="CTickets"),
    path('MTickets', MTickets, name="MTickets"),
    path('Registrar', Registrar, name="Registrar"),
    path('Ingresar', Ingresar, name="Ingresar"),
    path('Versiones', Versiones, name="Versiones"),
    path('Extensiones', Extensiones, name="Extensiones"),
    path('Skins', Skins, name="Skins"),
    path('Stash', Stash, name="Stash"),
]