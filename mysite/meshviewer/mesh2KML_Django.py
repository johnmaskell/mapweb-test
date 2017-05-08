import sys
#sys.path.append('C:/opentelemac-mascaret/v7p1/scripts/python27')
import os
import glob
from os import path
import numpy as np
# ~~> dependencies towards other modules
from config import OptionParser
# ~~> dependencies towards other modules
from parsers.parserSELAFIN import SELAFIN,SELAFINS,PARAFINS,subsetVariablesSLF
from parsers.parserFortran import cleanQuotes
from parsers.parserLQD import LQD
from parsers.parserKenue import InS
from utils.files import moveFile
from utils.progressbar import ProgressBar
from samplers.meshes import subdivideMesh
from converters import convertUTM as utm

from runSELAFIN import scanSELAFIN
import matplotlib.pyplot as plt
from matplotlib import tri
import matplotlib.cm as cm
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from pyproj import Proj, transform
import shutil
import re

def mesh2KML(meshFile,projection):
    if not os.path.isdir('static'):
        os.mkdir('static')
    else:
        # Remove old kml files
        for filename in glob.glob(os.path.join('static', '*.kml')):
            os.remove(filename) 
    fname = meshFile[:-3] + 'kml'
    print("fname before split" + fname)
    fname = fname.split("/")[2]
    #fname = "Mesh_Final_V1.kml"
    print("fname is " + fname)
    myFile = os.path.join('static',fname)
    print(myFile)
    fOut = open(myFile,'w')
    mainDir = 'static'
    inProj = Proj(init = projection)
    wgs = "epsg:4326"
    outProj = Proj(init = wgs)
    newScan = scanSELAFIN(meshFile)
    newScan.printHeader()
    
    slf = SELAFIN(meshFile)
    xmin = np.min(slf.MESHX) 
    xmax = np.max(slf.MESHX)
    ymin = np.min(slf.MESHY)
    ymax = np.max(slf.MESHY)
    elements = np.dstack((slf.MESHX[slf.IKLE2],slf.MESHY[slf.IKLE2]))
    mesh = np.array(slf.IKLE2)
    x = slf.MESHX
    y = slf.MESHY
    nelem = len(elements[:,0,0])
    inKml = mainDir + "/meshviewer/polyCell.kml"
    fIn = open(inKml,'r')
    lines = fIn.readlines()
    lcnt = 0
    for line in lines:
        if lcnt<47:
            fOut.write(line)
        lcnt = lcnt + 1
    cnt = 0
    
    for i in range(0,nelem):
        x1 = elements[i,0,0]
        y1 = elements[i,0,1]
        #if x1>=xmin and x1<=xmax and y1>=ymin and y1<=ymax:
        if i>=0:
            cnt = cnt + 1
            x2 = elements[i,1,0]
            y2 = elements[i,1,1]
            x3 = elements[i,2,0]
            y3 = elements[i,2,1]
            if projection != wgs:
                x1,y1 = transform(inProj,outProj,x1,y1)
                x2,y2 = transform(inProj,outProj,x2,y2)        
                x3,y3 = transform(inProj,outProj,x3,y3)
            poly = (str(x1)+","+str(y1)+","+str(0)+" "+str(x2)+","+str(y2)+","+str(0)+" "+str(x3)+","+str(y3)+","+str(0)+" "+str(x1)+","+str(y1)+","+str(0))
            fOut.write("<Placemark>" + "\n")
            fOut.write("<name>polyCell</name>" + "\n")
            fOut.write("<styleUrl>#msn_ylw-pushpin</styleUrl>" + "\n")
            fOut.write("<Polygon>" + "\n")
            fOut.write("<tessellate>1</tessellate>" + "\n")
            fOut.write("<altitudeMode>relativeToGround</altitudeMode>" + "\n")
            fOut.write("<outerBoundaryIs>" + "\n")
            fOut.write("<LinearRing>" + "\n")
            fOut.write("<coordinates>" + "\n")
            fOut.write(poly + "\n")
            fOut.write("</coordinates>" + "\n")
            fOut.write("</LinearRing>" + "\n")
            fOut.write("</outerBoundaryIs>" + "\n")
            fOut.write("</Polygon>" + "\n")
            fOut.write("</Placemark>" + "\n")
 
    fOut.write("</Document>" + "\n")
    fOut.write("</kml>" + "\n")
    fOut.close()
    fIn.close() 










