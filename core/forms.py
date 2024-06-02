from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Pedido, Producto

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

class SeleccionProductoForm(forms.Form):
    producto = forms.ModelChoiceField(queryset=Producto.objects.all(), label='Producto')
    cantidad = forms.IntegerField(label='Cantidad')

class ConfirmacionPersonalizacionForm(forms.Form):
    personalizacion = forms.CharField(widget=forms.Textarea, label='Personalización')

class MetodoEntregaForm(forms.Form):
    metodo_entrega = forms.ChoiceField(choices=[('tienda', 'Recoger en tienda'), ('domicilio', 'Entrega a domicilio')], label='Método de Entrega')

class PagoForm(forms.Form):
    metodo_pago = forms.ChoiceField(choices=[('tarjeta', 'Tarjeta de Crédito'), ('efectivo', 'Efectivo')], label='Método de Pago')
