import mongoengine
from django.core.validators import RegexValidator
from mongoengine import *
# from mongoengine.django import AbstractBaseUser

ROLE = (('PROFESSIONNEL', 'Professionnel'),
        ('ARTISTE', 'Artiste'))


def _not_empty(val):
    if not val:
        raise ValidationError('Champs requis')


class User(Document):
    id = StringField(required=True, unique=True)
    username = StringField(max_length=20, required=True, validation=_not_empty,
                           validators=[RegexValidator("[A-Za-z0-9@#$%^&+=]{8,}",
                                                      'Le mot de passe doit contenir '
                                                      'au moins 8 caractères sans espace'),
                                       _not_empty])
    first_name = StringField(max_length=40, required=True, validation=_not_empty)
    last_name = StringField(max_length=40, required=True, validation=_not_empty)
    email=StringField(max_length=40, required=True, validation=_not_empty)
    spotify = StringField(max_length=50)
    instagram = StringField(max_length=50)
    description = StringField(max_length=200, required=True, validation=_not_empty)
    avatar = ImageField(default='logo.png')
    role = StringField(choices=ROLE)
    password = StringField(max_length=50, required=True, validation=_not_empty)

# user = User(email='elwizmeziani85@gmail.com', password='projetweb@')
# user.save()

class Reservation(Document):
    id = StringField(required=True, unique=True)
    datetime_fin = DateTimeField(required=True)
    datetime_debut = DateTimeField(required=True)
    user = ReferenceField(User, reverse_delete_rule=mongoengine.CASCADE)