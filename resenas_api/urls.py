from django.urls import path
from . import views

urlpatterns = [
    path('resenas/', views.lista_resenas, name='lista_resenas'),
]