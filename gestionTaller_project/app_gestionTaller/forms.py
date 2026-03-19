from django import forms
from .models import Cliente, Coche, Servicio


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = "__all__"


class CocheForm(forms.ModelForm):
    class Meta:
        model = Coche
        fields = "__all__"


class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = "__all__"

