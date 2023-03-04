from django import forms
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
# from mongodbforms import EmbeddedDocumentForm, DocumentForm
class ReservationForm(forms.Form):
    datetime_debut = forms.DateField(widget=forms.DateTimeInput())
    datetime_fin = forms.DateField(widget=forms.DateTimeInput())

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control  col-4 text-white'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control  col-4 '}))

class RegisterForm(UserCreationForm):
        email = forms.EmailField(required=True, label='Adresse éléctronique', widget=forms.EmailInput(
            attrs={'class': 'form-control col-4', 'placeholder': 'user@gmail.com'}))
        last_name = forms.CharField(required=True, label='Nom',
                                    widget=forms.TextInput(attrs={'class': 'form-control col-4'}))
        first_name = forms.CharField(required=True, label='Prénom',
                                     widget=forms.TextInput(attrs={'class': 'form-control col-4'}))
        adresse = forms.CharField(required=True, label='Adresse',
                                  widget=forms.Textarea(attrs={'class': 'form-control col-4'}))
        code_postal = forms.CharField(required=True, label='Code postal',
                                      widget=forms.TextInput(attrs={'class': 'form-control col-4'}))
        telephone = forms.CharField(required=True, max_length=15, label='Téléphone',
                                    widget=forms.TextInput(attrs={'class': 'form-control col-4'}))
        avatar = forms.ImageField(label='Avatar',
                                  widget=forms.ClearableFileInput(attrs={'class': 'form-control col-4'}))

        # class Meta:
        #     model = User
        #     fields = (
        #     "username", "first_name", "last_name", "adresse", "code_postal", "email", "avatar", "role", "telephone")
