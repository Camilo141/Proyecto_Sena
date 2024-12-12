from django import forms
from .models import DetallePedido, Pedido
from inventario.models import Product

#class PedidoForm(forms.ModelForm):
#    class Meta:
#        model = DetallePedido
#        fields = ['telefono', 'direccion', 'ciudad', 'cantidad']
#        widgets = {
#            'telefono': forms.TextInput(attrs={'placeholder': 'Teléfono'}),
#            'direccion': forms.TextInput(attrs={'placeholder': 'Dirección'}),
#            'ciudad': forms.TextInput(attrs={'placeholder': 'Ciudad'}),
#            'cantidad': forms.NumberInput(attrs={'placeholder': 'Cantidad'}),
#        }


class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['direccion_envio', 'telefono', 'ciudad']

# Seleccionar Productos

class AgregarAlCarritoForm(forms.ModelForm):
    cantidad = forms.IntegerField(min_value=1, initial=1)

    class Meta:
        model = DetallePedido
        fields = ['producto', 'cantidad']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['producto'].queryset = Product.objects.filter(stock__gt=0)



class ConfirmarPedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['direccion_envio', 'telefono', 'ciudad']  #