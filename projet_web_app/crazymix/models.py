import mongoengine
from django.core.validators import RegexValidator
from mongoengine import *
import crazymix
from django.contrib.auth.models import AbstractUser

ROLE = (('PROFESSIONNEL', 'Professionnel'),
        ('ARTISTE', 'Artiste'))


def _not_empty(val):
    if not val:
        raise ValidationError('Champs requis')


class Utilisateur(Document):
    # id = StringField(required=True, unique=True)
    username = StringField(max_length=20, validation=_not_empty)
                           # validators=[RegexValidator("[A-Za-z0-9@#$%^&+=]{8,}",
                           #                            'Le mot de passe doit contenir '
                           #                            'au moins 8 caractères sans espace'),
                           #             _not_empty])
    first_name = StringField(max_length=40, required=True, validation=_not_empty)
    last_name = StringField(max_length=40, required=True, validation=_not_empty)
    email=StringField(max_length=40, required=True, validation=_not_empty)
    spotify = StringField(max_length=50,required=False)
    instagram = StringField(max_length=50)
    description = StringField(max_length=200, validation=_not_empty)
    avatar = ImageField(upload_to='img/',blank=True,null=True)
    role =StringField(choices=ROLE, required=True, validation=_not_empty)
    password = StringField(max_length=250, required=True, validation=_not_empty,validators=[RegexValidator("[A-Za-z0-9@#$%^&+=]{8,}",
                                                      'Le mot de passe doit contenir '
                                                      'au moins 8 caractères sans espace'),
                                       _not_empty])

class Reservation(Document):
    id = StringField(required=True, unique=True)
    datetime_fin = DateTimeField(required=True)
    datetime_debut = DateTimeField(required=True)
    user = ReferenceField(Utilisateur, reverse_delete_rule=mongoengine.CASCADE)
    # def __string__(self):
    #         return '%s' % (Utilisateur.username,)
class MyUser(AbstractUser):
    def __str__(self):
        return self.username
