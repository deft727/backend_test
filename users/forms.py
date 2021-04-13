
from django import forms
# from django.contrib.auth.models import User
from .models import User

# doing very simple registration
class RegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    password=forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(required=True)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].label='login'
        self.fields['password'].label = 'password'
        self.fields['email'].label='email'
        self.fields['confirm_password'].label='confirm_password'

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError(f'This e-mail is already registered')
        return self.cleaned_data['email']

    def clean_username(self):
        username= self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'name {username} exists')
        return username
    
    def clean(self):
        password = self.cleaned_data['password']
        confirm_password= self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('Password mismatch')
        return self.cleaned_data

    class Meta:
        model=User
        fields=['username','email','password','confirm_password',]

