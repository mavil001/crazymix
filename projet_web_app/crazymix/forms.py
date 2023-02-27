from django import forms
#from .models import User
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm


# class UserForm(forms.ModelForm):
#         class Meta:
#             model = User
#             fields = ("username", "first_name", "last_name", "spotify" "instagram", "avatar",
#                       "password1", "password2", "role", "description")

# class ReservationForm(forms.Form):
#
#     ReservationChoices=[
#         ('reserver une session','reserver une session'),
#         ('Mes sessions', 'Mes sessions')
#     ]
#     Reservation=forms.CharField(label='Reservation',widget=forms.Select(choices=ReservationChoices))


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control  col-4 '}))
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
