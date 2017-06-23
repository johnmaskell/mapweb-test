import sys
sys.path.append('C:/opentelemac-mascaret/v7p1/scripts/python27/')
from runSELAFIN import scanSELAFIN
from parsers.parserSELAFIN import SELAFIN
import numpy as np
from pyproj import Proj, transform
import os, glob


class BCOBJECT:
    def init __init__(self,bcfile,**kwargs):
        '''Reading a Telemac boundary conditions file (.cli) and converting the format and reprojecting etc'''
        self.bcfile = bcfile
        self.useropts = kwargs
        if self.fileExists():
            self.hcode,self.ucode,self.vcode,self.tcode,self.nodeno,self.bndryno,self.bname = self.parseBCFILE()



    def fileExists(self):
        goodpath = True
        if not os.path.isfile(self.bcfile):
            goodpath = False
        return goodpath

    def parseBCFILE(self):
        f = open(self.bcfile,'r')
        lines = f.readlines()
        f.close()
        hcode = []
        ucode = []
        vcode = []
        tcode = []
        nodeno = []
        bndryno = []
        bname = []

        for line in lines:
            splitline = line.split()
            hcode.append(splitline[0])
            ucode.append(splitline[1])
            vcode.append(splitline[2])
            tcode.append(splitline[7])
            nodeno.append(splitline[11])
            bndryno.append(splitline[12])
            bname.append(splitline[14])
        return

   
            
            
