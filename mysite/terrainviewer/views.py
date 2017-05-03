from django.shortcuts import render
from django.http import HttpResponse
import json
from pyproj import Proj, transform
#from testcoord import readCoord
# Create your views here.

inProj = Proj(init = "epsg:3857")
outProj = Proj(init = "epsg:4326")


def user_map(request):
    if request.is_ajax():
        #do something
        #request_data = request.POST
        #myPoly = request.POST.getlist('myPoly[]')
        #print(myPoly)
        #data_dict = json.loads(request.POST.get('jasonText'))
        #print(data_dict)
        #arr = request.POST.get('arr[]')
        #data_dict = json.dumps(arr)
        
        arr = json.loads(request.body)
        print(arr)
        x1,y1 = transform(inProj,outProj,float(arr[0]),float(arr[1]))
        print(str(x1) + ", " + str(y1))
        
        #print(data_dict['hint']['asdf'])
        #print data_dict['hint']['asdf'] 

        #print(request_data['myKey'])
        return HttpResponse("OK")
    return render(request,'terrainviewer/base.html')
    
