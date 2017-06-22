# Create your views here.
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from forms import FilterForm, DocumentForm,TitleForm,OutputVarForm,BndryCondsForm,ResultsForm,TimeStep,OutStep,Duration,InitConds,InitValue,TidalFlats,OptTidalFlats,OptLiquidBndry,TidalDatabase,AutoTune,AutoTuneOpts,BottomFric,MobileAlert
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
import os
import json
from telemactools.meshtools import MESHOBJECT

# Create your views here.

def display_map(request):
    errorMessage = None
    geodata = {}
    geodata = json.dumps(geodata)
    if request.method == 'POST':
        form1 = DocumentForm(request.POST, request.FILES)
        form = FilterForm(request.POST)
        bndryform = BndryCondsForm(request.POST,request.FILES)
        
        if form1.is_valid() and bndryform.is_valid():
            form1.save()
            bndryform.save()
            meshpath = request.FILES['document']
            bcpath = request.FILES['bndryfile']
            kwargs = {}
            kwargs["proj"] = request.POST['projection']
            cwd = os.getcwd()
            meshpath = cwd + '/documents/' + str(meshpath)
            bcpath = cwd + '/documents/' + str(bcpath)
            kwargs["bcfile"] = bcpath
            print(meshpath)
            #meshpath = 'C:/North_Sea_Model_v1/Mesh_Final_V1.slf'
            mymesh = MESHOBJECT(meshpath,**kwargs)
            if not mymesh.fileExists:    
                IOError('%s does not exist. Check file name and path' % self.meshfile)
                errorMessage = ('%s does not exist. Check file name and path' % self.meshfile)       
            else:                               
                meshgeojson = mymesh.mesh2GEOJSON()
                geodata = json.dumps(meshgeojson)
                meshcentre = mymesh.meshCentre()
                bndrysgeojson = mymesh.bndry2GEOJSON()                
                #return HttpResponseRedirect(reverse('model_parameters',args=[geodata]))
                request.session['my_data'] = geodata
                meshcentrestr = str(meshcentre[0]) + ","+ str(meshcentre[1])
                request.session['centre'] = meshcentrestr
                request.session['bndrysgeojson'] = bndrysgeojson
                return HttpResponseRedirect(reverse('model_parameters'))
    else:
        form1 = DocumentForm()
        bndryform = BndryCondsForm()
        form = FilterForm()
        

    
    return render(request,'runtide/fileuploadv2.html', {'form':form,'form1':form1,'geodata':geodata,'errorMessage':errorMessage,'bndryform':bndryform,})


    
def model_parameters(request):
    if request.method == 'POST':
        titleform = TitleForm(request.POST)        
        outvarform = OutputVarForm(request.POST)
        resform = ResultsForm(request.POST)
        tstepform = TimeStep(request.POST)
        outstepform = OutStep(request.POST)
        durform = Duration(request.POST)
        initcondform = InitConds(request.POST)
        initcondvalform = InitValue(request.POST)
        tidalflatsform = TidalFlats(request.POST)
        opttidalflatsform = OptTidalFlats(request.POST)
        optliqbndryform = OptLiquidBndry(request.POST)
        tidaldbform = TidalDatabase(request.POST)
        autotuneform = AutoTune(request.POST)
        autotuneoptsform = AutoTuneOpts(request.POST,request.FILES)
        bottomfric = BottomFric(request.POST)
        mobilealert = MobileAlert(request.POST)
        if autotuneoptsform.is_valid():
            autotuneoptsform.save()
            mytitle = request.POST['title']
            print(mytitle)
            for key, value in request.POST.items():
                print(key, value)
            
    else:
        titleform = TitleForm()
        outvarform = OutputVarForm()        
        resform = ResultsForm()
        tstepform = TimeStep()
        outstepform = OutStep()
        durform = Duration()
        initcondform = InitConds()
        initcondvalform = InitValue()
        tidalflatsform = TidalFlats({'tidalflats':'yes'})
        opttidalflatsform = OptTidalFlats({'opttidalflats':'1','optnegdepths':'1'})
        optliqbndryform = OptLiquidBndry()
        tidaldbform = TidalDatabase()
        autotuneform = AutoTune()
        autotuneoptsform = AutoTuneOpts()
        bottomfric = BottomFric()
        mobilealert = MobileAlert()
    geodata = request.session.get('my_data', None)
    meshcentre = request.session.get('centre', None)
    bndrysgeojson = request.session.get('bndrysgeojson')
    northbndry = json.dumps(bndrysgeojson['northbndry'])
    southbndry = json.dumps(bndrysgeojson['southbndry'])   
    
    return render(request,'runtide/modelforms.html',{'geodata':geodata,'northbndry':northbndry,'southbndry':southbndry,'meshcentre':meshcentre,'titleform':titleform,'outvarform':outvarform,'resform':resform,
                                                     'tstepform':tstepform,'outstepform':outstepform,'durform':durform,'initcondform':initcondform,'initcondvalform':initcondvalform,
                                                     'tidalflatsform':tidalflatsform,'opttidalflatsform':opttidalflatsform,'optliqbndryform':optliqbndryform,'tidaldbform':tidaldbform,'autotuneform':autotuneform,
                                                     'autotuneoptsform':autotuneoptsform,'bottomfric':bottomfric,'mobilealert':mobilealert,})












