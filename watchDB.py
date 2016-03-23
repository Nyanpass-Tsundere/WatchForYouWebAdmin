from setting import w_log as wDir, z_loc as zDB, areas
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

        return [0,sKey,'sucessful generate session key']
    
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
                    if watchID is None:
                        sFile.write(dataLine)
                    else:
                        if not watchID == json.loads(dataLine)[0]:
                            sFile.write(dataLine)
            sFile.close()
            return True
        except:
            sFile = open(path.join(wDir,watchSession.filename), 'w')
            sFile.close()

class watch:
    noSessionFile = 'notInSession'
    def sent(watchID,watchSessionkey,watchLoc,watchBS):
            logdata = [strftime('%Y-%m-%d_%H%M%S'),watchLoc,watchBS]
            
            try:
                watchManager.getName(watchID)
            except:
                return [-2,"Watch not register"]

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
            return [-1,"noname",'',"not register"]
        try:
            sFile = open(path.join(wDir,watchSession.filename) , 'r' )
        except:
            sFile = open(path.join(wDir,watchSession.filename) , 'a' )

        name = watchManager.getName(watchID)

        for line in sFile:
            content = json.loads(line)
            if content[0] == watchID:
                sFile.close()
                return [1,name,content[1],"a session to fetch"]
            
        sFile.close()
        return [0,name,'',"nothing to fetch"]

    def register(watchID,Name):
        watchDir = path.join(wDir,watchID)
        try :
            mkdir( watchDir )

            wFile = open( path.join(watchDir,watchNameFile), 'w' )
            wFile.writelines(Name)
            wFile.close()
            return [0,Name,"register sucesfull"]
        except:
            return [-1,Name,"register failed"]

class watchManager:
    from setting import t_format as timeFormat
    logEXT = ".log"

    def getName(watchID):
        wFile = open( path.join(wDir,watchID,watchNameFile), 'r' )
        return wFile.readline().split("\r")[0]

    def getPos(watchID,line = 1):
        import subprocess 
        from io import BytesIO
        session = watch.fetch(watchID)
        if session[0] == 0:
            filename = watch.noSessionFile
        else :
            filename = session[2]

        logFile = path.join(wDir,watchID,filename+watchManager.logEXT)

        lFile = open(logFile,'a')
        lFile.close()
        
        ## for python 3.5
        #process = subprocess.run(['tail',logFile,'-n '+str(int(line))],stdout=subprocess.PIPE)
        #buf = BytesIO(process.stdout)

        ## for python 3.2
        buf = BytesIO( subprocess.check_output(['tail',logFile,'-n '+str(int(line))]) )
        data = []
        for line in buf.readlines():
            loadline = json.loads(line.decode())
            data.append(  [loadline[0],loadline[1]] )

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

class zone:
    import sqlite3
    table_prefix = 'Map'
    def genTableName(MapID):
        return zone.table_prefix + str(int(MapID))

    def checkZoneTable(MapID):
        TableName = zone.genTableName(MapID)
        with zone.sqlite3.connect(zDB) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('SELECT * FROM '+TableName)
            except:
                return [-1,'table not exist']
                
            conn.close
        return [0,'table exist']

    def createZoneTable(MapID):
        TableName = zone.genTableName(MapID)
        with zone.sqlite3.connect(zDB) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('CREATE TABLE '+TableName+ \
                        ' (Name UNIQUE, PosLT, PosRB, alwaysAlert Boolean, PRIMARY KEY (PosLT,PosRB))')
            except:
                return [-1,'create table failed']
            conn.close

        return [0,'create sucessful']

    def newZone(MapID,name,X,Y,alwaysAlert=False):
        tableName = zone.genTableName(MapID)
        value = [name,X,Y,alwaysAlert]
        with zone.sqlite3.connect(zDB) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('INSERT INTO '+tableName+' (Name,PosLT,PosRB,closeBlock,alwaysAlert) VALUES (?,?,?,?);',value)
            except:
                return [-1,'create zone record failed']
            conn.commit()
            conn.close
        return [0,'Create zone record sucessful']

    def listZone(MapID):
        TableName = zone.genTableName(MapID)
        with zone.sqlite3.connect(zDB) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('SELECT * FROM '+TableName)
            except:
                return [-1,'table not exist']
            data = cursor.fetchall()
            conn.close
        return [0,data]
            

    def inZone(MapID,X,Y):
        data = zone.listZone(MapID)
        if data[0] < 0:
            return [-2,'fetch zone failed']

        data = data[1]
        includeZones = []
        counter = 0
        for zoneLine in data:
            if eval(zoneLine[1])[0] < X and \
            eval(zoneLine[2])[0] > X and \
            eval(zoneLine[1])[1] < Y and \
            eval(zoneLine[2])[1] > Y :
                includeZones.append(zoneLine)
                counter+=1

        return [counter,includeZones]

