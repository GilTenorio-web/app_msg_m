from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, ClearableFileInput, widgets
from django import forms
from users_manager.models import Archivo, CustomUser

class ProfileForm(ModelForm):
    
    class Meta:
        # TO DO: MOVE VARIABLES TO OUTER CLASS
        user_name=forms.CharField()
        last_name=forms.CharField()
        nick_name=forms.CharField()
        user_email=forms.EmailField()
        password=forms.CharField(widget=forms.PasswordInput)
        user_age=forms.IntegerField()
        model=CustomUser
        widgets={
            'user_name': forms.TextInput(attrs={'placeholder': 'Nombre'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Apellido'}),
            'nick_name': forms.TextInput(attrs={'placeholder': 'Nickname'}),
            'user_email': forms.TextInput(attrs={'placeholder': 'Correo electronico'}),
            'password': forms.PasswordInput(attrs={'placeholder':'Contraseña'}),
            'user_age': forms.TextInput(attrs={'placeholder': 'Edad'}),
        }
        fields='__all__'

class SignupForm(UserCreationForm):
    
    class Meta:
        model=User
        fields=('username','password1','password2')

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['placeholder'] = 'nick-name'
        self.fields['password1'].widget.attrs['placeholder'] = 'contraseña'
        self.fields['password2'].widget.attrs['placeholder'] = 'contraseña'

class CustomClearableFileInput(ClearableFileInput):
    template_with_clear = '<br>  <label for="%(clear_checkbox_id)s">%(clear_checkbox_label)s</label> %(clear)s'

class FormArchivos(ModelForm):
    file = forms.FileField()
    class Meta:
        model=Archivo
        fields=[
            'name',
            'user',
            'file'
        ]
        labels={
            'name': 'Nombre de archivo',
            'user': 'Usuario',
            'file': 'Archivo',
        }

        widgets={
            'file': CustomClearableFileInput,
            'user': forms.Select
        }



        

