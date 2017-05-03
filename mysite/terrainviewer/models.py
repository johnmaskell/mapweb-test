from django.db import models

# Create your models here.

class Adminupload(models.Model):
    author = models.ForeignKey('auth.User')

class Meshbinupload(models.Model):
    meshbin = models.FileField(upload_to = 'documents/')
    meshbinid = models.ForeignKey(Adminupload)

class Renderoneupload(models.Model):
    renderone = models.FileField(upload_to = 'documents/')
    renderoneid = models.ForeignKey(Adminupload)
    
class Rendertwoupload(models.Model):
    rendertwo = models.FileField(upload_to = 'documents/')
    rendertwoid = models.ForeignKey(Adminupload)


    
    
