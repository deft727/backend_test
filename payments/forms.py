from django import forms
from .models import Order


class OrderPayForm(forms.Form):
    stripe_token = forms.CharField(max_length=100, widget=forms.HiddenInput)
    address = forms.CharField(max_length=255)


class OrderForm(forms.ModelForm):

    class Meta:
        model= Order
        fields = ('address',)
        