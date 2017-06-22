from django import forms
from .models import Document,BCFile,ObsFile

class FilterForm(forms.Form):
    CHOICES = (('epsg:4326', 'EPSG:4326'),('epsg:27700', 'EPSG:27700'),)
    projection = forms.ChoiceField(choices=CHOICES)
    
class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('document',)
        labels = {"document":"Upload mesh file"}

class TitleForm(forms.Form):
    title = forms.CharField(max_length=100,label='Title',initial = 'Enter a title',required=False)

class OutputVarForm(forms.Form):
        OPTIONS = (
                ("U", "U-Current (m/s)"),
                ("V", "V-Current (m/s)"),
                ("S", "Elevation (m)"),
                ("H", "Water Depth (m)"),
                )
        outputvar = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                             choices=OPTIONS,label='Output variables')

class BndryCondsForm(forms.ModelForm):
    class Meta:
        model = BCFile
        fields = ('bndryfile',)
        labels = {"bndryfile":"Upload boundary conditions file"}

        
class ResultsForm(forms.Form):
    resfile = forms.CharField(max_length=100,label='Results file',initial = 'Name results file (e.g. myresults.slf',required=False)

class TimeStep(forms.Form):
    tstep = forms.IntegerField(label='Time step',initial = 'Enter time-step',required=False)

class OutStep(forms.Form):
    outint = forms.IntegerField(label='Output interval',required=False)
    OPTIONS = (
                ("hours", "Hours"),
                ("minutes", "Minutes"),
                ("seconds", "Seconds"),                
                )
    outunits = forms.CharField(label='units', widget=forms.Select(choices=OPTIONS))

class Duration(forms.Form):
    startdate = forms.CharField(max_length=50,label='Start date',initial='YYYY/MM/DD HH:MM:SS',required=False)
    enddate = forms.CharField(max_length=50,label='End date',initial='YYYY/MM/DD HH:MM:SS',required=False)
    
class InitConds(forms.Form):

    OPTIONS = (
                ("zeroelevation", "Zero Elevation"),
                ("constantelevation", "Constant Elevation"),                
                ("zerodepth", "Zero Depth"),
                ("constantdepth", "Constant Depth"),
                )
    initcond = forms.ChoiceField(widget=forms.RadioSelect,
                                             choices=OPTIONS,label='Initial conditions')

class InitValue(forms.Form):
    initval = forms.FloatField(label='Inital value (metres)',initial = 'Enter value',required=False)
    

class TidalFlats(forms.Form):

    OPTIONS = (
                ("yes", "Yes"),
                ("no", "No"),               
                )
    
    tidalflats = forms.ChoiceField(widget=forms.RadioSelect,
                                             choices=OPTIONS,label='Tidal flats')

class OptTidalFlats(forms.Form):
    OPTIONS = (
                ("1", "1"),
                ("2", "2"),               
                )
    
    opttidalflats = forms.ChoiceField(widget=forms.RadioSelect,
                                             choices=OPTIONS,label='Option for tidal flat treatment')
    
    CHOICES = (
                ("1", "1"),
                ("2", "2"),
                ("3", "3"),
                )


    optnegdepths = forms.ChoiceField(widget=forms.RadioSelect,
                                             choices=CHOICES,label='Option for negative depth treatment')


class OptLiquidBndry(forms.Form):
        OPTIONS = (
                ("1", "Strong setting"),
                ("2", "Thompson method"),               
                )
        bndryi = forms.ChoiceField(widget=forms.RadioSelect,
                                             choices=OPTIONS,label='Option for liquid boundary (1)')
        bndryii = forms.ChoiceField(widget=forms.RadioSelect,
                                             choices=OPTIONS,label='Option for liquid boundary (2)')
    


class TidalDatabase(forms.Form):
    CHOICES = (('1', 'JMJ'),('2', 'TPXO'),('3', 'Misc.'),)
    tidaldatabase = forms.ChoiceField(choices=CHOICES)


class AutoTune(forms.Form):
    OPTIONS = (
                ("1", ""),                               
                )
    autocalib = forms.ChoiceField(widget=forms.RadioSelect,
                                             choices=OPTIONS,label='Automatic calibration')

class AutoTuneOpts(forms.ModelForm):    
    class Meta:
        model = ObsFile
        fields = ('obsfldr','noiters')
        labels = {"obsfldr":"Upload observations zip file.","noiters":"No. of iterations"} 

     
    





    
