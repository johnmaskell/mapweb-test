from django import forms

class XminCoord(forms.Form):
    xmin = forms.CharField(initial="",label="Xmin")

class YminCoord(forms.Form):
    ymin = forms.CharField(initial="",label="Ymin")

class XmaxCoord(forms.Form):
    xmax = forms.CharField(initial="",label="Xmax")

class YmaxCoord(forms.Form):
    ymax = forms.CharField(initial="",label="Ymax")



   

        
