################################################################
#                                                              #
# Author: John Maskell                                         #
# Date: 30/09/16                                               #
#                                                              #
# Create a wkt file from GE kml to cut bathy data in qgs.      #
#                                                              #
# Inputs:                                                      #
# KML poly                                                     #
#                                                              #
#                                                              #


#___Imports________________________________________

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cbook
from matplotlib import cm
from matplotlib.colors import LightSource
import matplotlib
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import os
import sys
import glob
from pyproj import Proj, transform
import shutil
import re

#___Functions______________________________________

def kml2Poly(kmlFile):
    lcnt = 0
    f = open(kmlFile,'r')
    fileContent = f.readlines()
    for line in fileContent:
        if "<coordinates>" in line:
            coords = fileContent[lcnt+1]        
            splitCoords = coords.split(" ")
            xpoly = np.zeros(len(splitCoords))
            ypoly = np.zeros(len(splitCoords))
            polygon = np.zeros((len(splitCoords),2))
            cnt = 0
            for numSet in splitCoords:
                sepCoord = numSet.split(",")
                if len(sepCoord)>1:
                    xstring = re.sub("[^-9-9.-e]", "", sepCoord[0])
                    ystring = re.sub("[^-9-9.-e]", "", sepCoord[1])                    
                    xpoly[cnt] = float(xstring)
                    ypoly[cnt] = float(ystring)
                    polygon[cnt,0] = xpoly[cnt]
                    polygon[cnt,1] = ypoly[cnt]
                    print(str(xpoly[cnt]) + " " + str(ypoly[cnt]))
                    cnt = cnt + 1
        lcnt = lcnt + 1
    f.close()        
    return xpoly[:cnt], ypoly[:cnt], polygon[:cnt,:]


def writeWkt(outFile,xpoly,ypoly):
    f = open(outFile,'w')
    f.write("id;wkt" + "\n")
    f.write("1;POLYGON((")
    for i in range(0, len(xpoly)):
        if i<len(xpoly)-1:
            f.write(str(xpoly[i]) + " " + str(ypoly[i]) + ",")
        else:
            f.write(str(xpoly[i]) + " " + str(ypoly[i]))
    f.write("))")
    f.close()


#____Main________________________________________


            
    














