from django import forms


class FilterForm(forms.Form):
    CHOICES = (('greyscale', 'Greyscale/Hillshade'),('colour', 'Colour'),)
    myRender = forms.ChoiceField(choices=CHOICES, label="Render")
    
    
class CoordForm(forms.Form):
    myCoords = forms.CharField(initial="Your Coords",label="Coordinates")
   

        
