from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import json
from pyproj import Proj, transform
from forms import FilterForm, CoordForm
#from testcoord import readCoord
# Create your views here.
import os
inProj = Proj(init = "epsg:3857")
outProj = Proj(init = "epsg:27700")

test = 1
def user_map(request):
    #os.chdir(os.path.dirname(__file__))
    #pageMessage = None
    pageMessage = None

    if request.method == 'POST':
        #arr = json.loads(request.body) 
        form = FilterForm(request.POST)
        form1 = CoordForm(request.POST)
        print("Hello")
        if form.is_valid() or form1.is_valid():

            rend = request.POST['myRender']
            coords = request.POST['myCoords']

            print(rend)
            print(coords)

            x1 = float(coords.split(",")[0])
            print(str(x1))
            y1 = float(coords.split(",")[1])

            
            #arr = json.loads(request.body)
            #for key in request.POST:
            #    print(key)
            #   value = request.POST[key]
            #    print(value)
            #test = request.POST['csrfmiddlewaretoken']
            #print("This - " + test)
            
            
            #rend = request.POST['myRender']
            
            #print("Attay[0] - " + str(arr[0]))
            #print(rend)
            #arr = [1,2,3,4]
            x1,y1 = transform(inProj,outProj,x1,y1)
            #print(str(x1) + ", " + str(y1))
        #temporary test are for 3d model
        #threshold is 10 km
            thold = 10000.
            data_av = False
            lakes_xo = 322173.0;lakes_yo = 515831.0;
            walton_xo = 620000.0; walton_yo = 220000.0;

        #test if it is near the lakes model
            dist = ((x1-lakes_xo)**2+(y1-lakes_yo)**2)**0.5
            if dist<=thold:
                data_av = True
        #test if it is near the lakes model
            dist = ((x1-walton_xo)**2+(y1-walton_yo)**2)**0.5
            if dist<=thold:
                data_av = True

            if data_av:
                pageMessage = "3D Terrain model available"
                return render(request,'terrainviewer/north_lakes_render.html')
            else:
                pageMessage = "No 3D Terrain model available"
        
            print(pageMessage)         
        #return HttpResponseRedirect("http://127.0.0.1:8000/terrainviewer/tester")
    else:
        form = FilterForm()
        form1 = CoordForm()
    return render(request,'terrainviewer/selectionMessage.html', {'form1':form1,'form':form,'pageMessage':pageMessage,})
    
