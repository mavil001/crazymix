from django import forms
from .models import User
from django.contrib.auth.forms import AuthenticationForm

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


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control  col-4 text-white'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control  col-4 '}))