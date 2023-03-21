from django import forms
#from .models import User
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm

from crazymix.models import ROLE,Utilisateur



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

class RegisterForm(forms.Form):
        username= forms.CharField( label="Nom d'utilisateur",
                                    widget=forms.TextInput(attrs={'class': 'form-control col-4'}))
        password= forms.CharField(required=True, label='Mot de passe',
                                    widget=forms.PasswordInput(attrs={'class': 'form-control col-4'}))
        password1=forms.CharField(required=True, label='confirmation mot de passe',
                                    widget=forms.PasswordInput(attrs={'class': 'form-control col-4'}))
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
        spotify= forms.CharField(required=False,label='Spotify',
                                     widget=forms.TextInput(attrs={'class': 'form-control col-4', 'placeholder':'facultatif'}))
        instagram = forms.CharField( required=False,label='Instagram',
                                  widget=forms.TextInput(attrs={'class': 'form-control col-4','placeholder':'facultatif'}))
        description = forms.CharField(required=True, label='Description',
                                  widget=forms.Textarea(attrs={'class': 'form-control col-4'}))
        role= forms.ChoiceField(required=True,choices=ROLE, widget=forms.Select)

        # class Meta:
        #     model = User
        #     fields = (
        #     "username", "first_name", "last_name", "adresse", "code_postal", "email", "avatar", "role", "telephone")


class ModifierProfilForm(forms.Form):

    id=forms.CharField(widget=forms.HiddenInput())
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
    spotify = forms.CharField(required=False, label='Spotify',
                              widget=forms.TextInput(
                                  attrs={'class': 'form-control col-4', 'placeholder': 'facultatif'}))
    instagram = forms.CharField(required=False, label='Instagram',
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control col-4', 'placeholder': 'facultatif'}))
    description = forms.CharField(required=True, label='Description',
                                  widget=forms.Textarea(attrs={'class': 'form-control col-4'}))
    role = forms.ChoiceField(required=True, choices=ROLE, widget=forms.Select)

    def __init__(self,*args, **kwargs):
        instance = kwargs.pop('instance', None)

        if instance:
            initial = {
                'id': instance.id,
                'email': instance.email,
                'last_name': instance.last_name,
                'first_name': instance.first_name,
                'adresse': instance.adresse,
                'code_postal': instance.code_postal,
                'telephone': instance.telephone,
                'avatar': instance.avatar,
                'spotify': instance.spotify,
                'instagram': instance.instagram,
                'description': instance.description,
                'role': instance.role,
            }
           # initial['id'] = instance.id
           # initial['last_name'] = instance.last_name
           # initial['first_name'] = instance.first_name
           # initial['telephone'] = instance.telephone
           # initial['email'] = instance.email
           # initial['code_postal'] = instance.code_postal
           # initial['adresse'] = instance.adresse
           # initial['avatar'] = instance.avatar
           # initial['spotify'] = instance.spotify
           # initial['instagram'] = instance.instagram
           # initial['description'] = instance.description
           # initial['role'] = instance.role


            kwargs['initial'] = initial
            super().__init__(*args, **kwargs)
       # super().__init__(*args, **kwargs)




class ModifierContactForm(forms.Form):

    id=forms.CharField(widget=forms.HiddenInput())

    email = forms.EmailField(required=True, label='Adresse éléctronique', widget=forms.EmailInput(
        attrs={'class': 'form-control col-4', 'placeholder': 'user@gmail.com'}))
    telephone = forms.CharField(required=True, max_length=15, label='Téléphone',
                                widget=forms.TextInput(attrs={'class': 'form-control col-4'}))
    spotify = forms.CharField(required=False, label='Spotify',
                              widget=forms.TextInput(
                                  attrs={'class': 'form-control col-4', 'placeholder': 'facultatif'}))
    instagram = forms.CharField(required=False, label='Instagram',
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control col-4', 'placeholder': 'facultatif'}))

    def __init__(self, *args, **kwargs):
        instance = kwargs.pop('instance', None)

        if instance:
            initial = {
                'id': instance.id,

                 'email': instance.email,
                'telephone': instance.telephone,
                'spotify': instance.spotify,
                'instagram': instance.instagram
            }
            kwargs['initial'] = initial
            super().__init__(*args, **kwargs)


class ModifierInfoPersoForm(forms.Form):

    id=forms.CharField(widget=forms.HiddenInput())
    avatar = forms.ImageField(label='Avatar',
                              widget=forms.ClearableFileInput(attrs={'class': 'form-control col-4'}))
    last_name = forms.CharField(required=True, label='Nom',
                                widget=forms.TextInput(attrs={'class': 'form-control col-4'}))
    first_name = forms.CharField(required=True, label='Prénom',
                                 widget=forms.TextInput(attrs={'class': 'form-control col-4'}))

    def __init__(self, *args, **kwargs):
        instance = kwargs.pop('instance', None)

        if instance:
            initial = {
                'id': instance.id,
                'avatar': instance.avatar,
                'last_name': instance.last_name,
                'first_name': instance.first_name
            }
            kwargs['initial'] = initial
            super().__init__(*args, **kwargs)


class ModifierAdresseForm(forms.Form):

    id=forms.CharField(widget=forms.HiddenInput())

    adresse = forms.CharField(required=True, label='Adresse',
                              widget=forms.Textarea(attrs={'class': 'form-control col-4'}))
    code_postal = forms.CharField(required=True, label='Code postal',
                                  widget=forms.TextInput(attrs={'class': 'form-control col-4'}))

    description = forms.CharField(required=True, label='Description',
                                  widget=forms.Textarea(attrs={'class': 'form-control col-4'}))
    role = forms.ChoiceField(required=True, choices=ROLE, widget=forms.Select)
    def __init__(self, *args, **kwargs):
        instance = kwargs.pop('instance', None)

        if instance:
            initial = {
                'id': instance.id,

                'adresse': instance.adresse,
                'code_postal': instance.code_postal,
                'description': instance.description,
                'role': instance.role
            }
            kwargs['initial'] = initial
            super().__init__(*args, **kwargs)

class ModifierMdpForm(forms.Form):

    id=forms.CharField(widget=forms.HiddenInput())

    ancienMdp = forms.CharField(required=True, label=' Ancien mot de passe',
                               widget=forms.PasswordInput(attrs={'class': 'form-control col-4'}))
    nouveaumotpasse = forms.CharField(required=True, label='Nouveau mot de passe',
                               widget=forms.PasswordInput(attrs={'class': 'form-control col-4'}))

    confirmatioMdp = forms.CharField(required=True, label='Confirmation mot de passe',
                               widget=forms.PasswordInput(attrs={'class': 'form-control col-4'}))

    def __init__(self, *args, **kwargs):
        instance = kwargs.pop('instance', None)

        if instance:
            initial = {
                'id': instance.id,

                'password': instance.password

            }
            kwargs['initial'] = initial
            super().__init__(*args, **kwargs)