from mongoengine import *

class User(Document):
   username = StringField()
   first_name=StringField()
   last_name=StringField()

