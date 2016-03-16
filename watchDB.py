from setting import w_log as wDir
import json
from os import path, mkdir, listdir
from time import strftime 

watchNameFile = 'name.txt'

class watchSession:
    filename = 'sessions.txt'
    from setting import t_format as timeFormat
    
    
    def chkWatchDir(watchID):
        ## init dir
        if not path.isdir(wDir):
            mkdir(wDir)

        ## init watch's dir
        watchDir = path.join(wDir,watchID)
        if not path.isdir(watchDir):
            return False
        else:
            return True

    def new(watchID,expireTime,permission = None ):
        ## init watch dir if not exist
        ## just convient for debug
        watchSession.chkWatchDir(watchID)

        ## clean exist session
        watchSession.clean(watchID)

        ## Generator Session
        sKey = strftime(watchSession.timeFormat)
        sData = [watchID,sKey,expireTime,permission]

        sFile = open(path.join(wDir,watchSession.filename) , 'a' )
        sFile.writelines(json.dumps(sData)+ "\n")
        sFile.close()

        return sKey
    
    def check(watchID,Key):
        sFile = open(path.join(wDir,watchSession.filename) , 'r' )
        
        for line in sFile:
            content = json.loads(line)
            if content[0] == watchID and content[1] == Key:
                sFile.close()
                return True

        sFile.close()
        return False

    def clean(watchID = None):
        try:
            sFile = open(path.join(wDir,watchSession.filename), 'r')
            data = sFile.readlines()
            sFile.close

            sFile = open(path.join(wDir,watchSession.filename), 'w')
        
            for dataLine in data:
                if not strftime(watchSession.timeFormat) > json.loads(dataLine)[2] :
                    if watchID == None:
                        sFile.write(dataLine)
                    else:
                        if not watchID == json.loads(dataLine)[0]:
                            sFile.write(dataLine)

            sFile.close
            return True
        except:
            sFile = open(path.join(wDir,watchSession.filename), 'w')
            sFile.close

class watch:
    noSessionFile = 'notInSession'
    def sent(watchID,watchSessionkey,watchLoc,watchBS):
            logdata = [strftime('%Y-%m-%d_%H%M%S'),watchLoc,watchBS]

            logFile = open( path.join(wDir,watchID,watchSessionkey+watchManager.logEXT) ,'a')
            logFile.writelines(json.dumps(logdata)+"\n")
            logFile.close()

            watchSession.clean()
            if watchSession.check(watchID,watchSessionkey):
                return [1,"update Sucessful"]
            else:
                return [0,"Updated, but Session already End"]

    def fetch(watchID):
        if not watchSession.chkWatchDir(watchID):
            return [-1,"noname","not register"]
        try:
            sFile = open(path.join(wDir,watchSession.filename) , 'r' )
        except:
            sFile = open(path.join(wDir,watchSession.filename) , 'a' )

        name = watchManager.getName(watchID)

        for line in sFile:
            content = json.loads(line)
            if content[0] == watchID:
                sFile.close()
                return [1,name,"a session to fetch",content[1]]
            
        sFile.close()
        return [0,name,"nothing to fetch"]

    def register(watchID,Name):
        watchDir = path.join(wDir,watchID)
        try :
            mkdir( watchDir )

            wFile = open( path.join(watchDir,watchNameFile), 'w' )
            wFile.writelines(Name)
            wFile.close
            return [0,Name,"register sucesfull"]
        except:
            return [-1,Name,"register failed"]

class watchManager:
    from setting import t_format as timeFormat
    logEXT = ".log"

    def getName(watchID):
        wFile = open( path.join(wDir,watchID,watchNameFile), 'r' )
        return wFile.readline()

    def getPos(watchID,line = 1):
        import subprocess 
        from io import BytesIO
        session = watch.fetch(watchID)
        if session[0] == 0:
            filename = watch.noSessionFile
        else :
            filename = session[2]

        logFile = path.join(wDir,watchID,filename+watchManager.logEXT)
        
        ## for python 3.5
        #process = subprocess.run(['tail',logFile,'-n '+str(int(line))],stdout=subprocess.PIPE)
        #buf = BytesIO(process.stdout)

        ## for python 3.2
        buf = BytesIO( subprocess.check_output(['tail',logFile,'-n '+str(int(line))]) )
        data = []
        for line in buf.readlines():
            data.append(json.loads(line.decode()))

        return data


    def listDir(tDir):
        return [ name for name in listdir(tDir) if path.isdir(path.join(tDir, name)) ]

    def watchs():
        return watchManager.listDir(wDir)

    def actWatchs():
        sFile = open( path.join(wDir,watchSession.filename) , 'r')
        sessions = []
        for line in sFile.readlines():
            sessions.append(json.loads(line))
        
        watchs = []
        for session in sessions:
            watchs.append(session[0])
        
        return watchs
