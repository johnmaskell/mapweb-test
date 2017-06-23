import os
import numpy as np
from datetime import datetime, timedelta






class CASFILE:
    def __init__(self,postdic):
        '''Generate a Telemac steering file from the user entered paramters'''
        self.postdic = postdic
        if not self.postdic['title']=="":
            self.filelead = self.postdic['title'].replace(" ","")
        else:
            ext = self.genfileExt()
            self.filelead = "T2Dtidalrun" + ext
        print(self.filelead)
        
    def genfileExt(self):
        now = datetime.now()    
        snow = str(now)    
        datesplit = snow.split("-")
        yr = datesplit[0]
        yr = yr[2:4]    
        mn = datesplit[1]
        dy = (datesplit[2].split(" "))[0]
        timesplit = snow.split(":")
        hr = (timesplit[0].split(" "))[1]    
        mi = timesplit[1]
        se = (timesplit[2].split("."))[0]
        ext = yr + mn + dy + hr + mi + se
        return ext

    def writeCasfile(self):
        cwd = os.getcwd()
        casstr = self.casfileString()
        title = (self.postdic['title'])
        meshfile = (self.postdic['meshfile']).replace("/","\\")
        bcfile = (self.postdic['bcfile']).replace("/","\\")
        if not self.postdic['resfile']=="":
            resfile = self.postdic['resfile'].replace(" ","")
        else:
            resfile = self.filelead + ".slf"       
        outvars = self.postdic['outputvar']
        outvars = [s.encode('ascii') for s in outvars]
        outvarsstr = ""
        for var in outvars:
            outvarsstr+= (var + ",")
        outvarsstr = outvarsstr[:-1]    
        timestep = float(self.postdic['tstep'])
        outint = self.calcOutint()
        print(str(outint))
        nsteps = self.calcNsteps()
        initcond = self.postdic['initcond']
        tideflat = self.postdic['tidalflats']
        opttideflat = int(self.postdic['opttidalflats'])
        negdepth = int(self.postdic['optnegdepths'])
        optliqbndry = self.postdic['bndryi'] + ";" + self.postdic['bndryii']
        opttide = int(self.postdic['tidaldatabase'])
        origdate = (((self.postdic['startdate']).split(" "))[0]).replace("/",";")
        origtime = (((self.postdic['startdate']).split(" "))[1]).replace(":",";")
        friclaw = int(self.postdic['friclaw'])
        print(self.postdic['friccoef'])
        if self.postdic['friccoef'] == '':
            self.postdic['friccoef']=0.0
        friccoef = float(self.postdic['friccoef'])

        outcas = (casstr % (title,meshfile,bcfile,resfile,outvarsstr,timestep,nsteps,outint,initcond,tideflat,opttideflat,negdepth,optliqbndry,opttide,origdate,origtime,friclaw,friccoef))
        outfile = cwd + '/documents/' + self.filelead + ".str"
        f = open(outfile,'w')
        f.write(outcas)
        f.close()


    def calcNsteps(self):
        tformat = '%Y/%m/%d %H:%M:%S'
        print(self.postdic['startdate'])
        start_time = datetime.strptime(self.postdic['startdate'],tformat)
        end_time = datetime.strptime(self.postdic['enddate'],tformat)
        simtimesecs = (end_time-start_time).total_seconds()
        nsteps = int(simtimesecs/float(self.postdic['tstep']))
        return nsteps

    def calcOutint(self):
        if self.postdic['outunits'] == 'hours':
            interval = int((float(self.postdic['outint'])*3600.)/float(self.postdic['tstep']))
        if self.postdic['outunits'] == 'minutes':
            interval = int((float(self.postdic['outint'])*60.)/float(self.postdic['tstep']))
        if self.postdic['outunits'] == 'seconds':
            interval = int((float(self.postdic['outint']))/float(self.postdic['tstep']))

        #interval has to be at least as big as time-step
        interval = np.max([interval,float(self.postdic['tstep'])])
        return interval
        
        











    def casfileString(self):
        casstr = '''TITLE = '%s'
/--------------------------------------------------
/     GENERAL OPTIONS
/--------------------------------------------------
FORTRAN FILE                : 'myBordllv7p0r1.f'
FORMATTED DATA FILE 1       : 'mesh2UTM30N.txt'
BOUNDARY CONDITIONS FILE           : %s
GEOMETRY FILE                      : %s
/GEOMETRY FILE FORMAT : 'SERAFIN '
RESULTS FILE                     : %s
BINARY DATABASE 1 FOR TIDE  : h_tpxo7.2
BINARY DATABASE 2 FOR TIDE  : u_tpxo7.2
CHECKING THE MESH = true
/DEBUGGER = 1

/--------------------------------------------------
VARIABLES FOR GRAPHIC PRINTOUTS  : '%s'
TIME STEP                                       : %f
NUMBER OF TIME STEPS                            : %d
GRAPHIC PRINTOUT PERIOD                         : %d
LISTING PRINTOUT PERIOD                         : 120
MASS-BALANCE                                    : YES
/--------------------------------------------------
INITIAL CONDITIONS                              : '%s'
SPATIAL PROJECTION TYPE : 1
SPHERICAL COORDINATES = NO
/LATITUDE OF ORIGIN POINT = 48.6667
LATITUDE OF ORIGIN POINT = 49.28
/--------------------------------------------------
TIDAL FLATS                                     : %s
/THRESHOLD FOR VISCOSITY CORRECTION ON TIDAL FLATS: 0.D0
OPTION FOR THE TREATMENT OF TIDAL FLATS         : %d
/ TO HAVE POSITIVE DEPTHS EVERYWHERE
TREATMENT OF NEGATIVE DEPTHS                    : %d
OPTION FOR LIQUID BOUNDARIES                    : %s
/--------------------------------------------------
/                       TIDE CONDITIONS
/--------------------------------------------------
OPTION FOR TIDAL BOUNDARY CONDITIONS            : 1;1
TIDAL DATA BASE                                 : %d
ORIGINAL DATE OF TIME                           : %s       
ORIGINAL HOUR OF TIME                           : %s 
GEOGRAPHIC SYSTEM	                        : 2
ZONE NUMBER IN GEOGRAPHIC SYSTEM                : 30
COEFFICIENT TO CALIBRATE TIDAL RANGE            : 1.0

/--------------------------------------------------
/    PROPAGATION
/--------------------------------------------------
/PROPAGATION STEP                                : YES
/--------------------------------------------------
/     SOURCE TERMS
/--------------------------------------------------
/BOTTOM SMOOTHINGS                     : 2
LAW OF BOTTOM FRICTION                          : %d
FRICTION COEFFICIENT                            : %f 
DISCRETIZATIONS IN SPACE                        : 11 ; 11 
MATRIX STORAGE                                  : 3
FREE SURFACE GRADIENT COMPATIBILITY             : 0.5
/
TREATMENT OF THE LINEAR SYSTEM                  : 2
/
TYPE OF ADVECTION                               : 1;5
SUPG OPTION                                     : 0;0
/
SOLVER                                          : 1
SOLVER ACCURACY                                 : 1.E-4
MAXIMUM NUMBER OF ITERATIONS FOR SOLVER         : 500
PRECONDITIONING                                 : 2
SOLVER OPTION                                   : 3
/
/BOTTOM SMOOTHINGS                              : 0
ZERO                                            : 1.E-10


MASS-LUMPING ON H                               : 1.
CONTINUITY CORRECTION                           : YES


/&ETA
&FIN'''
        return casstr
