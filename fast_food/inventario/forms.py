from django import forms
from ventas.models import Pedido, DetallePedido

#class PedidoForm(forms.ModelForm):
#    class Meta:
#        model = Pedido
#        fields = ['direccion_envio']
#        labels = {
#            'direccion_envio': 'Dirección de Envío',}

class PedidoForm(forms.ModelForm):
    class Meta:
        model = DetallePedido
        fields = ['telefono', 'direccion', 'ciudad']
        labels = {
            'telefono': 'Telefono','direccion':'Direccion','ciudad':'Ciudad'
        }

