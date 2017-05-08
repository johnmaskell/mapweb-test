import math
from numpy import exp, cos, linspace
import matplotlib.pyplot as plt
import os, time, glob

def dummyFile():
    if not os.path.isdir('static'):
        os.mkdir('static')
    else:
        # Remove old plot files
        for filename in glob.glob(os.path.join('static', '*.txt')):
            os.remove(filename)        
        
    
    myFile = os.path.join('static','dummyFile.txt')
    f = open(myFile,'w')
    f.write("This is a dummy file!")
    f.close()
    return myFile
