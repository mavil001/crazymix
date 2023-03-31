import mongoengine
from django.core.validators import RegexValidator
from mongoengine import *
from mongoengine import Document, fields
import crazymix
from django.contrib.auth.models import AbstractUser
from django.core.files.storage import FileSystemStorage
import subprocess,os
ROLE = (('PROFESSIONNEL', 'Professionnel'),
        ('ARTISTE', 'Artiste'))
STATUT=(('EN_ATTENTE', 'En attente'),
        ('VALIDE', 'Validé'),
        ('COMPLETE', 'Complété'))

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
    adresse=StringField(max_length=250, required=True, validation=_not_empty)
    email=StringField(max_length=40, required=True, validation=_not_empty)
    telephone = StringField(max_length=40, required=True, validation=_not_empty)
    spotify = StringField(max_length=50,required=False)
    instagram = StringField(max_length=50)
    description = StringField(max_length=200, validation=_not_empty)
    code_postal=StringField(max_length=40, required=True, validation=_not_empty)
    avatar = ImageField(upload_to='img/',blank=True,null=True)
    role =StringField(choices=ROLE, required=True, validation=_not_empty)
    password = StringField(max_length=250, required=True, validation=_not_empty,validators=[RegexValidator("[A-Za-z0-9@#$%^&+=]{8,}",
                                                      'Le mot de passe doit contenir '
                                                      'au moins 8 caractères sans espace'),
                                       _not_empty])


class Reservation(Document):
    pass


class Enregistrement(Document):
    path=StringField(required=True)
    reservation=ReferenceField(Reservation, reverse_delete_rule=mongoengine.CASCADE, required=True)
    
class Reservation(Document):
    fin = DateTimeField(required=True)
    debut = DateTimeField(required=True)
    user = ReferenceField(Utilisateur, reverse_delete_rule=mongoengine.CASCADE, required=True)
    statut=StringField(choices=STATUT, required=True)
    enregistrement = ReferenceField(Enregistrement, reverse_delete_rule=mongoengine.CASCADE)


class MyUser(AbstractUser):
    def __str__(self):
        return self.username

class ExtraitAudio(Document):
    utilisateur=ReferenceField(Utilisateur, reverse_delete_rule=mongoengine.CASCADE, required=True)
    audio = fields.FileField()

    # def save(self, *args, **kwargs):
    #     super(ExtraitAudio, self).save(*args, **kwargs)
    #
    #     if self.audio and not self.extrait:
    #         fss = FileSystemStorage()
    #         audio_path = fss.path(self.audio.name)
    #         extrait_path = os.path.splitext(audio_path)[0] + '_extrait.mp3'
    #
    #         subprocess.run(
    #             ['ffmpeg', '-i', audio_path, '-ss', '00:00:30', '-t', '00:00:10', '-acodec', 'copy', extrait_path],
    #             check=True)
    #
    #         with open(extrait_path, 'rb') as f:
    #             self.audio.put(f, content_type='audio/mp3')
    #             self.save()
