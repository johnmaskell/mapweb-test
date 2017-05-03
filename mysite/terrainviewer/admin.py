from django.contrib import admin
from .models import Adminupload, Meshbinupload, Renderoneupload, Rendertwoupload

# Register your models here.
myModels = [Adminupload,Meshbinupload,Renderoneupload,Rendertwoupload] 
admin.site.register(myModels)

