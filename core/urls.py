from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
# path('', , name=""),

urlpatterns = [
    path('', views.Principal, name='Principal'),
    path('comprar/', views.Comprar, name='Comprar'),
    path('soporte/', views.Soporte, name='Soporte'),
    path('crear_ticket/', views.CTickets, name='CTickets'),
    path('mis_tickets/', views.MTickets, name='MTickets'),
    path('mi_perfil/', views.Perfil, name="Perfil"),
    path('registrar/', views.Registrar, name='Registrar'),
    path('login/', LoginView.as_view(template_name='core/ingresar.html'), name='Ingresar'),
    path('logout/', LogoutView.as_view(next_page='Principal'), name='logout'),
    path('recuperar_contrasena', views.Recuperar, name="Recuperar"),
    path('versiones/', views.Versiones, name='Versiones'),
    path('extensiones/', views.Extensiones, name='Extensiones'),
    path('extensiones/<str:categoria>/', views.Extensiones, name='extensiones_categoria'),
    path('skins/', views.Skins, name='Skins'),
    path('stash/', views.Stash, name='Stash'),
    path('perfil/', views.Perfil, name='perfil'),
    path('exito/', views.exito, name='exito'),
]