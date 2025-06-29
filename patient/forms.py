from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django import forms
from .models import CustomUser

# Custom User Creation Form
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Nom d’utilisateur',
                'maxlength': 150,
                'pattern': '[a-zA-Z0-9@.+-]+',
                'title': 'Utilisez uniquement des lettres, chiffres et @/./+/-/'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Adresse e-mail',
                'type': 'email'
            }),
            'phone_number': forms.TextInput(attrs={
                'placeholder': 'Numéro de téléphone',
                'pattern': '[0-9]+',
                'title': 'Utilisez uniquement des chiffres',
                'maxlength': 10
            }),
            'password1': forms.PasswordInput(attrs={
                'placeholder': 'Mot de passe',
                'minlength': 8,
                'title': 'Le mot de passe doit comporter au moins 8 caractères'
            }),
            'password2': forms.PasswordInput(attrs={
                'placeholder': 'Confirmer le mot de passe',
                'minlength': 8
            }),
        }

# Custom Authentication Form
class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser

# Patient Update Form
class PatientUpdateForm(UserChangeForm):
    password = None  # Exclude the password field from the form

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }
