from django.contrib import admin

# Register your models here.
from .models import PerfilUsuario, Version, Skins, AgrandarAlijo, Ticket, Pve, Compra, Resena

admin.site.register(PerfilUsuario)
admin.site.register(Version)
admin.site.register(Skins)
admin.site.register(AgrandarAlijo)
admin.site.register(Ticket)
admin.site.register(Pve)
admin.site.register(Compra)
admin.site.register(Resena)