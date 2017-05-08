from datetime import datetime

##########################################################
#
#Generate a unique file extention based on the date/time
#
##########################################################


def genfileExt():
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
