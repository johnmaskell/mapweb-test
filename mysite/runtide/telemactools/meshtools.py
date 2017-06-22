import sys
sys.path.append('C:/opentelemac-mascaret/v7p1/scripts/python27/')
from runSELAFIN import scanSELAFIN
from parsers.parserSELAFIN import SELAFIN
import numpy as np
from pyproj import Proj, transform
import os, glob




class MESHOBJECT:
    def __init__(self,meshfile,**kwargs):
        '''Reading a Telemac mesh and converting the format and reprojecting etc'''
        self.meshfile = meshfile
        self.useropts = kwargs
        if self.fileExists():        
            self.slf = SELAFIN(meshfile)
            self.xmesh = self.slf.MESHX
            self.ymesh = self.slf.MESHY
            self.elements = self.slf.IKLE2
        if "bcfile" in self.useropts:
            self.bcfile = kwargs["bcfile"]
            print(self.bcfile)

    def meshCentre(self):
        oldproj = self.useropts['proj']
        newproj = 'EPSG:3857'
        xnew,ynew = self.meshReproj(oldproj,newproj)
        meshcentre = np.zeros(2)
        meshcentre[0] = np.mean(xnew)
        meshcentre[1] = np.mean(ynew)
        return meshcentre

    def meshReproj(self,oldproj,newproj):
        inProj = Proj(init=oldproj)
        outProj = Proj(init=newproj)
        xnew,ynew = transform(inProj,outProj,self.xmesh,self.ymesh)
        return xnew, ynew
                
    def fileExists(self):
        goodpath = True
        if not os.path.isfile(self.meshfile):
            goodpath = False
        return goodpath

    def mesh2GEOJSON(self):
        geojson = {}
        oldproj = self.useropts['proj']
        newproj = 'EPSG:3857'
        xnew,ynew = self.meshReproj(oldproj,newproj)
        coords = []
        outer = []
        for i in range(len(self.elements)):
            poly = []
            outer = []
            for j in range(0,3):               
                node = [(xnew[self.elements[i,j]]),(ynew[self.elements[i,j]])]
                poly.append(node)
            outer.append(poly)
            coords.append(outer)
        geojson["type"] = "FeatureCollection"
        crslist = {}
        crslist["type"] = "name"
        crsprops = {}
        crsprops["name"] = "EPSG:3857"
        crslist["properties"] = crsprops
        geojson["crs"] = crslist
        featarr = []
        featlist = {}
        featlist["type"] = "Feature"
        geolist = {}
        geolist["type"] = "MultiPolygon"
        geolist["coordinates"] = coords
        featlist["geometry"] = geolist
        featarr.append(featlist)
        geojson["features"] = featarr       
        
        return(geojson)

    def delMeshes(self):
        path = (self.meshfile.split("/"))
        print(path)
        flist = glob.glob((self.meshfile.split("/"))[:-1] + "*.slf")
        for slffile in flist:
            print(slffile)
        
         

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
            if int(splitline[0]) > 2:
                hcode.append(splitline[0])
                ucode.append(splitline[1])
                vcode.append(splitline[2])
                tcode.append(splitline[7])
                nodeno.append(splitline[11])
                bndryno.append(splitline[12])
                bname.append(splitline[14])
        return hcode,ucode,vcode,tcode,nodeno,bndryno,bname
        
        
        
    def bndry2GEOJSON(self):
        hcode,ucode,vcode,tcode,nodeno,bndryno,bname = self.parseBCFILE()
        oldproj = self.useropts['proj']
        newproj = 'EPSG:3857'
        xnew,ynew = self.meshReproj(oldproj,newproj)
        bnameset = set(bname)
        bnamenew = list(bnameset)
        bndrysgeojson = {}
        for obndry in bnamenew:
            coords = []
            coordarr = []
            geojson = {}
            for i in range(0,len(bname)):
                if bname[i] == obndry:
                    node = [xnew[int(nodeno[i])-1],ynew[int(nodeno[i])-1]]                    
                    coords.append(node)
            coordarr.append(coords)        
            geojson["type"] = "FeatureCollection"
            crslist = {}
            crslist["type"] = "name"
            crsprops = {}
            crsprops["name"] = "EPSG:3857"
            crslist["properties"] = crsprops
            geojson["crs"] = crslist
            featarr = []
            featlist = {}
            featlist["type"] = "Feature"
            geolist = {}
            geolist["type"] = "MultiLineString"
            geolist["coordinates"] = coordarr
            featlist["geometry"] = geolist
            featarr.append(featlist)
            geojson["features"] = featarr 
            bndrysgeojson[obndry] = geojson
        return bndrysgeojson

                
    
        
                
                
            
                
        
                
