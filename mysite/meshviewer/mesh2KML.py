# _____          ___________________________________________________
# ____/ Imports /__________________________________________________/
#
# ~~> dependencies towards standard python
import sys
import os
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

mainDir = 'C:/windFarm/'
f = mainDir + 'wind_farm_mesh_02.slf'

newScan = scanSELAFIN(f)

newScan.printHeader()

slf = SELAFIN(f)
xmin = np.min(slf.MESHX) 
xmax = np.max(slf.MESHX)
ymin = np.min(slf.MESHY)
ymax = np.max(slf.MESHY)
elements = np.dstack((slf.MESHX[slf.IKLE2],slf.MESHY[slf.IKLE2]))
mesh = np.array(slf.IKLE2)
x = slf.MESHX
y = slf.MESHY

print(elements.shape)

print(str(len(elements[:,0,0])))

nelem = len(elements[:,0,0])

xmin = 532000.
xmax = 538000.
ymin = 338000.
ymax = 343000.

fOut = open(mainDir + "kml/wind_farm_mesh_02.kml",'w')

inKml = mainDir + "kml/polyCell.kml"
fIn = open(inKml,'r')
lines = fIn.readlines()
lcnt = 0
for line in lines:
    if lcnt<47:
        fOut.write(line)
    lcnt = lcnt + 1

inProj = Proj(init = 'epsg:27700')
outProj = Proj(init = 'epsg:4326')

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
        #x1,y1 = transform(inProj,outProj,x1,y1)
        #x2,y2 = transform(inProj,outProj,x2,y2)        
        #x3,y3 = transform(inProj,outProj,x3,y3)
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
        #if cnt==4:
            #break

fOut.write("</Document>" + "\n")
fOut.write("</kml>" + "\n")
fOut.close()
fIn.close() 

