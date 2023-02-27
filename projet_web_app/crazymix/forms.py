from django import forms
from .models import User
from django import forms

# class UserForm(forms.ModelForm):
#         class Meta:
#             model = User
#             fields = ("username", "first_name", "last_name", "spotify" "instagram", "avatar",
#                       "password1", "password2", "role", "description")

# class ReservationForm(forms.Form):
#     todo = forms.CharField(
#         widget=forms.TextInput(attrs={"class": "form-control"}))
#     date = forms.DateField(
#         widget=DateTimePicker(options={"format": "YYYY-MM-DD",
#                                        "pickTime": False}))
#     reminder = forms.DateTimeField(
#         required=False,
#         widget=DateTimePicker(options={"format": "YYYY-MM-DD HH:mm",
#                                        "pickSeconds": False}))

# class ReservationForm(forms.Form):
#
#     ReservationChoices=[
#         ('reserver une session','reserver une session'),
#         ('Mes sessions', 'Mes sessions')
#     ]
#     Reservation=forms.CharField(label='Reservation',widget=forms.Select(choices=ReservationChoices))