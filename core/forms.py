# core/forms.py

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Pedido

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['fecha_entrega', 'direccion_entrega']


class RegistroForm(UserCreationForm):
    direccion = forms.CharField(max_length=255, required=True)
    telefono = forms.CharField(max_length=20, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'direccion', 'telefono']
