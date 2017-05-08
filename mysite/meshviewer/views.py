from django.shortcuts import render
from models import Document, Proj
from forms import FilterForm
from forms import DocumentForm
from django.http import HttpResponse
import os
from dummy import dummyFile
from mesh2KML_Django import mesh2KML
from wsgiref.util import FileWrapper
# Create your views here.

def model_form_upload(request):
    os.chdir(os.path.dirname(__file__))
    answer = None
    result = None
    if request.method == 'POST':
        form1 = DocumentForm(request.POST, request.FILES)
        form = FilterForm(request.POST)        
        if form1.is_valid() or form.is_valid():
            form1.save()
            proj = request.POST['projection']
            myfile = request.FILES['document']            
            meshname = str(myfile)
            result = meshname[:-3] + "kml"
            cwd = os.getcwd()
            meshFile = cwd + '/documents/' + str(myfile)
            mesh2KML(meshFile,proj)
            
    else:
        form1 = DocumentForm()
        form = FilterForm()
    return render(request,'meshviewer/fileupload.html', {'form1':form1,'result':result,'form':form,
                                                         'answer':answer,})


            
  
