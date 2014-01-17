from django.contrib.auth.models import User
from django.db import models
from oauth2client.django_orm import CredentialsField


class UserGoogleID(models.Model):
    user = models.ForeignKey(User)
    googleplus_id = models.TextField()
#    display_id = models.TextField()

class CredentialsModel(models.Model):
    id = models.ForeignKey(User, primary_key=True)
    credential = CredentialsField()
