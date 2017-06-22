from __future__ import unicode_literals

from django.db import models

# Create your models here.

# Create your models here.

class Document(models.Model):
    document = models.FileField(upload_to = 'documents/')

class BCFile(models.Model):
    bndryfile = models.FileField(upload_to = 'documents/')

class ObsFile(models.Model):
    obsfldr = models.FileField(upload_to = 'documents/')
    noiters = models.IntegerField(default=5)
