from setting import w_log as wDir
import json
from os import path , mkdir
from time import strftime 

class watchSession:
    filename = 'sessions.txt'
    from setting import t_format as timeFormat

    def new(watchID,expireTime,permission = None ):
        ## init dir
        if not path.isdir(wDir):
            mkdir(wDir)

        ## init watch's dir
        watchDir = path.join(wDir,watchID)
        if not path.isdir(watchDir):
            mkdir(watchDir)
        
        ## Generator Session
        sKey = strftime(watchSession.timeFormat)
        sData = [watchID,sKey,expireTime,permission]

        sFile = open(path.join(wDir,watchSession.filename) , 'a' )
        sFile.writelines(json.dumps(sData)+ "\n")
        sFile.close()

        return sKey
    
    def fetch(watchID):
        sFile = open(path.join(wDir,watchSession.filename) , 'r' )

        for line in sFile:
            content = json.loads(line)
            if content[0] == watchID:
                sFile.close()
                return content[1]
            
        sFile.close()
        return False

    def check(watchID,Key):
        sFile = open(path.join(wDir,watchSession.filename) , 'r' )
        
        for line in sFile:
            content = json.loads(line)
            if content[0] == watchID and content[1] == Key:
                sFile.close()
                return True

        sFile.close()
        return False

    def clean():
        sFile = open(path.join(wDir,watchSession.filename), 'r')
        data = sFile.readlines()
        sFile.close

        sFile = open(path.join(wDir,watchSession.filename), 'w')
        
        for dataLine in data:
            if not strftime(watchSession.timeFormat) > json.loads(dataLine)[2] :
                sFile.write(dataLine)

        sFile.close
        return True

class watchManager:

    from setting import t_format as timeFormat
    logEXT = ".log"
    
    def sent(watchID,watchSessionkey,watchLoc,watchBS):
        logdata = [strftime(watchManager.timeFormat),watchLoc,watchBS]

        logFile = open( path.join(wDir,watchID,watchSessionkey+watchManager.logEXT) ,'a')
        logFile.writelines(json.dumps(logdata)+"\n")
        logFile.close()

        watchSession.clean()
        if watchSession.check(watchID,watchSessionkey):
            return True
        else:
            return False

