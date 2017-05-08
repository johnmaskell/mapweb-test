from django import forms
from .models import Document, Proj


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('document',)
        labels = {"document":"Upload mesh file"}
class FilterForm(forms.Form):
    CHOICES = (('epsg:4326', 'EPSG:4326'),('epsg:27700', 'EPSG:27700'),)
    projection = forms.ChoiceField(choices=CHOICES)
    
    
    


        
