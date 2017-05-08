from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Document(models.Model):
    document = models.FileField(upload_to = 'documents/')
    

class Proj(models.Model):

    projval = models.CharField(max_length=200)

