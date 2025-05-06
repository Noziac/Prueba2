from django.urls import path
from . import views

urlpatterns = [
    path('resenas/', views.lista_resenas, name='lista_resenas'),
    path('resenas/<id>', views.vista_resenas, name='vista_resenas'),
]