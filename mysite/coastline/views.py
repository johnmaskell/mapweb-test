from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect
import json
from pyproj import Proj, transform
from forms import XminCoord,YminCoord,XmaxCoord,YmaxCoord
import os
import zipfile
import StringIO
from kmlpoly2Wkt import writeWkt
from fileExt import genfileExt
import os
inProj = Proj(init = "epsg:3857")
outProj = Proj(init = "epsg:4326")

coast_path = "C:\\Coastline\\GSHHS_shp\\i\\"
shape_file = "GSHHS_i_L1.shp"
doc_fldr = "/coastline/documents/"

def coast_extract(request):
    result = None
    if request.method == 'POST':       
        form = XminCoord(request.POST)
        form1 = YminCoord(request.POST)
        form2 = XmaxCoord(request.POST)
        form3 = YmaxCoord(request.POST)
        
        if form.is_valid() or form1.is_valid():

            xmin = request.POST['xmin']
            ymin = request.POST['ymin']
            xmax = request.POST['xmax']
            ymax = request.POST['ymax']
            xmin,ymin = transform(inProj,outProj,xmin,ymin)
            xmax,ymax = transform(inProj,outProj,xmax,ymax)
            cwd = os.getcwd()            
            fileext = genfileExt()                   
            newdir = cwd + "/coastline/static/coastline" + fileext + "/"
            os.makedirs(newdir)
            xpoly = [xmin,xmin,xmax,xmax,xmin]
            ypoly = [ymin,ymax,ymax,ymin,ymin]
            outFile = newdir + "coastline" + fileext + ".csv"
            writeWkt(outFile,xpoly,ypoly)
            sys_command = 'ogr2ogr -f "ESRI Shapefile" ' + newdir +"coastline" + fileext + ".shp " + coast_path + shape_file + " -clipsrc " + str(xmin) + " " + str(ymin) + " " + str(xmax) + " " + str(ymax)
            os.system(sys_command)
            filenames = os.listdir(newdir)
            zip_subdir = "coastline" + fileext + "zipped"
            zip_filename = "%s.zip" % zip_subdir
            s = StringIO.StringIO()
            zf = zipfile.ZipFile(s, "w")
            for fpath in filenames:
                fpath = newdir + fpath
           # Calculate path for file in zip
                fdir, fname = os.path.split(fpath)
                zip_path = os.path.join(zip_subdir, fname)
           # Add file, at correct path
                zf.write(fpath, zip_path)
            zf.close()
            # Grab ZIP file from in-memory, make response with correct MIME-type
            resp = HttpResponse(s.getvalue(), content_type = "application/x-zip-compressed")
            # ..and correct content-disposition
            resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

            return resp

            



    else:

        form = XminCoord()
        form1 = YminCoord()
        form2 = XmaxCoord()
        form3 = YmaxCoord()

        
    return render(request,'coastline/coast_extractor.html', {'form':form,'form1':form1,'form2':form2,'form3':form3,})
    
