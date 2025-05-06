from django.urls import path
from . import views

urlpatterns = [
    path('productos/', views.lista_productos, name='lista_productos'),

    path('productos/versiones/', views.lista_versiones, name='lista_versiones'),
    path('productos/skins/', views.lista_skins, name='lista_skins'),
    path('productos/pve/', views.lista_pve, name='lista_pve'),
    path('productos/alijos/', views.lista_alijos, name='lista_alijos'),
    
    path('productos/versiones/<id>/', views.vista_versiones, name='vista_version'),
    path('productos/skins/<id>/', views.vista_skins, name='vista_skin'),
    path('productos/pve/<id>/', views.vista_pve, name='vista_pve'),
    path('productos/alijos/<id>/', views.vista_alijos, name='vista_alijo'),
]