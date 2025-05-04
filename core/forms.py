from django import forms
from django.contrib.auth.models import User
from .models import PerfilUsuario, Ticket

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

class ComprarProductoForm(forms.Form):
    content_type = forms.CharField(widget=forms.HiddenInput())
    object_id = forms.IntegerField(widget=forms.HiddenInput())