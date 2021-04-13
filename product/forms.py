from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from django.conf import settings
from product.models import Like, Product,Comment

User = get_user_model()


class LikeForm(forms.Form):
    user = forms.ModelChoiceField(User.objects.all(), required=False)
    product = forms.ModelChoiceField(Product.objects.all())
    ip = forms.GenericIPAddressField(required=False)


class ReviewsForm(forms.ModelForm):

    class Meta:
        model= Comment
        fields=('text',)
