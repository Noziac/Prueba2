from django import forms
from django.contrib.auth.models import User
from .models import PerfilUsuario
from .models import Ticket

class EditarPerfilForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class EditarAvatarForm(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = ('avatar',)

class CrearTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['asunto', 'mensaje', 'prioridad']