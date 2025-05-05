from django import forms
from django.contrib.auth.models import User
from .models import PerfilUsuario, Ticket, Resena

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

class ResenaForm(forms.ModelForm):
    evaluacion = forms.IntegerField(min_value=1, max_value=10)

    class Meta:
        model = Resena
        fields = ['texto', 'evaluacion']
        widgets = {
            'texto': forms.Textarea(attrs={'rows': 3}),
        }