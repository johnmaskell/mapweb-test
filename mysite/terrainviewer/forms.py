from django import forms
from .models import Adminupload

class Meshbinform(forms.ModelForm):
    class Meta:
        model = Meshbinupload
        fields = ('document',)
        labels = {"document":"Upload a bin file"}

class Renderoneform(forms.ModelForm):
    class Meta:
        model = Renderoneupload
        fields = ('document',)
        labels = {"document":"Upload a shade render file"}

class Rendertwoform(forms.ModelForm):
    class Meta:
        model = Rendertwoupload
        fields = ('document',)
        labels = {"document":"Upload a colour render file"}
