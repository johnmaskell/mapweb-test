from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from forms import FilterForm,DocumentForm,TitleForm,OutputVarForm,BndryCondsForm,ResultsForm,TimeStep,OutStep,Duration,InitConds,InitValue,TidalFlats,OptTidalFlats,OptLiquidBndry,TidalDatabase,AutoTune,AutoTuneOpts,BottomFric,MobileAlert
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
import os
import json
import zipfile
from telemactools.meshtools import MESHOBJECT
from telemactools.filehandlers import CASFILE



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
            mymesh = MESHOBJECT(meshpath,**kwargs)
            if not mymesh.fileExists:    
                IOError('%s does not exist. Check file name and path' % self.meshfile)
                errorMessage = ('%s does not exist. Check file name and path' % self.meshfile)       
            else:                               
                meshgeojson = mymesh.mesh2GEOJSON()
                geodata = json.dumps(meshgeojson)
                meshcentre = mymesh.meshCentre()
                bndrysgeojson = mymesh.bndry2GEOJSON()                
                request.session['my_data'] = geodata
                meshcentrestr = str(meshcentre[0]) + ","+ str(meshcentre[1])
                request.session['centre'] = meshcentrestr
                request.session['bndrysgeojson'] = bndrysgeojson
                request.session['meshfile'] = meshpath
                request.session['bcfile'] = bcpath

                
                return HttpResponseRedirect(reverse('model_parameters'))
    else:
        form1 = DocumentForm()
        bndryform = BndryCondsForm()
        form = FilterForm()
        

    
    return render(request,'runtide/fileuploadv2.html', {'form':form,'form1':form1,'geodata':geodata,'errorMessage':errorMessage,'bndryform':bndryform,})


    
def model_parameters(request):
    errormsg = ""
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
        if tstepform.is_valid() and outvarform.is_valid() and outstepform.is_valid() and durform.is_valid() and initcondform.is_valid() and optliqbndryform.is_valid():
            postitems = {}
            #autotuneoptsform.save()
            mytitle = request.POST['title']
            outvars = request.POST.getlist('outputvar')
            for key, value in request.POST.items():
                print(key, value)
                postitems[key] = value
            postitems['meshfile'] = request.session.get('meshfile',None)
            postitems['bcfile'] = request.session.get('bcfile',None)
            postitems['outputvar'] = outvars
            mycasfile = CASFILE(postitems)
            mycasfile.writeCasfile()
            if 'autocalib' in postitems:
                if postitems['autocalib']=="1":
                    if autotuneoptsform.is_valid():
                        autotuneoptsform.save()                    
                        content = request.FILES['obsfldr']
                        cwd = os.getcwd()
                        dirname = cwd + "\\documents\\"
                        zippath = dirname + str(content)
                        zipobj = zipfile.ZipFile(zippath)
                        zipobj.extractall(dirname)
                        zipobj.close()
                        os.remove(zippath)
        else:
            errormsg = "Please fill in all the fields."
                    
                    
            
    else:
        titleform = TitleForm()
        outvarform = OutputVarForm()        
        resform = ResultsForm()
        tstepform = TimeStep()
        outstepform = OutStep()
        durform = Duration()
        initcondform = InitConds()
        initcondvalform = InitValue()
        tidalflatsform = TidalFlats({'tidalflats':'YES'})
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
    
    return render(request,'runtide/modelforms.html',locals())












