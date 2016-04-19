from setting import w_log as wDir, z_loc as zDB
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
        import pyqrcode
        from setting import qr_local_path as qrPath
        ## init watch dir if not exist
        ## just convient for debug
        watchSession.chkWatchDir(watchID)

        ## clean exist session
        watchSession.clean(watchID)

        ## Generator Session
        sKey = strftime(watchSession.timeFormat) + "-session" + "-" + watchID
        sData = [watchID,sKey,expireTime,permission]

        sFile = open(path.join(wDir,watchSession.filename) , 'a' )
        sFile.writelines(json.dumps(sData)+ "\n")
        sFile.close()

        if ( not path.exists(qrPath) ):
            mkdir(qrPath)

        url = pyqrcode.create(sKey,error='L')
        url.png(path.join(qrPath,sKey+'.png'), scale=8, module_color=[0, 0, 0, 255], background=[0xff, 0xff, 0xff])

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

    def list():
        sFile = open(path.join(wDir,watchSession.filename) , 'r' )
        
        allSession = []
        for line in sFile:
            content = json.loads(line)
            allSession.append(content)

        return allSession


    def clean(watchID = None):
        from setting import qr_local_path as qrPath
        from os import remove
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
                else:
                    remove(qrPath+json.loads(dataLine)[1]+'.png')


            sFile.close()
            return True
        except:
            sFile = open(path.join(wDir,watchSession.filename), 'w')
            sFile.close()

class watch:
    noSessionFile = 'notInSession'
    def sent(watchID,watchSessionkey,watchLoc,watchBS,moving = None):
            logdata = [strftime('%Y-%m-%d_%H%M%S'),watchLoc,watchBS,moving]
            
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

    def fetch(watchID,forWatch = None):
        from setting import qr_web_path as qrPath
        if not watchSession.chkWatchDir(watchID):
            return [-1,"noname",'',"not register"]
        try:
            watchSession.clean()
            sFile = open(path.join(wDir,watchSession.filename) , 'r' )
        except:
            sFile = open(path.join(wDir,watchSession.filename) , 'a' )

        name = watchManager.getName(watchID)

        for line in sFile:
            content = json.loads(line)
            if content[0] == watchID:
                sFile.close()
                if ( forWatch == True ):
                    return [1,name,qrPath+content[1]+'.png',"a session to fetch"]
                else:
                    return [1,name,content[1],"a session to fetch"]
            
        sFile.close()
        return [0,name,'',"nothing to fetch"]

    def register(watchID,Name):
        watchDir = path.join(wDir,watchID)
        try :
            mkdir( watchDir )

            if watch.naming(watchID,Name)[0] == 0:
                return [0,Name,"register sucesfull"]
            else:
                return [-1,Name,"naming failed"]
        except:
            return [-1,Name,"register failed"]

    def naming(watchID,Name):
        watchDir = path.join(wDir,watchID)
        try: 
            wFile = open( path.join(watchDir,watchNameFile), 'w' )
            wFile.writelines(Name)
            wFile.close()
            return [0,Name,'Naming Success']
        except:
            return [1,Name,'Naming Success']
        

class watchManager:
    from setting import t_format as timeFormat
    logEXT = ".log"

    def getName(watchID):
        wFile = open( path.join(wDir,watchID,watchNameFile), 'r' )
        return wFile.readline().split("\r")[0]

    def getPos(watchID,line = 1):
        session = watch.fetch(watchID)
        if session[0] == 0:
            filename = watch.noSessionFile
        else :
            filename = session[2]

        logFile = path.join(wDir,watchID,filename+watchManager.logEXT)
        
        from tail import tail
        return tail(logFile,line)

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
                        ' (Name UNIQUE, closeBlock, PosDoor, PosLT, PosRB, alwaysAlert Boolean, PRIMARY KEY (PosLT,PosRB))')
            except:
                return [-1,'create table failed']
            conn.close

        return [0,'create sucessful']

    def newZone(MapID,name,LT,RB,closeBlock=None,PosDoor=None,alwaysAlert=False):
        tableName = zone.genTableName(MapID)
        value = [name,closeBlock,PosDoor,LT,RB,alwaysAlert]
        with zone.sqlite3.connect(zDB) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('INSERT INTO '+tableName+' (Name,closeBlock,PosDoor,PosLT,PosRB,alwaysAlert) VALUES (?,?,?,?,?,?);',value)
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
                zone.createZoneTable(MapID)
                return [-1,'table not exist']
            data = cursor.fetchall()
            conn.close
        return [0,data]

    def setAlertZone(MapID,ZoneName,alert):
        TableName = zone.genTableName(MapID)
        with zone.sqlite3.connect(zDB) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('UPDATE '+TableName+' SET alwaysAlert = ? WHERE Name = ?;',[alert,ZoneName])
            except:
                return [-1,'something wrong']
            conn.commit
            conn.close
        return [0,"sucessful update"]

    def delZone(MapID,ZoneName):
        TableName = zone.genTableName(MapID)
        with zone.sqlite3.connect(zDB) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('DELETE FROM '+TableName+' WHERE Name = ?;',[ZoneName])
            except:
                return [-1,'something wrong']
            conn.commit
            conn.close
        return [0,"sucessful update"]

    def renameZone(MapID,ZoneName,ZoneNewName):
        TableName = zone.genTableName(MapID)
        with zone.sqlite3.connect(zDB) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('UPDATE '+TableName+' SET Name = ? WHERE Name = ?;',[ZoneNewName,ZoneName])
            except:
                return [-1,'something wrong']
            conn.commit
            conn.close
        return [0,"sucessful update"]

    def inZone(MapID,X,Y,AlertArea=False):
        data = zone.listZone(MapID)
        if data[0] < 0:
            return [-2,'fetch zone failed']

        data = data[1]
        includeZones = []
        counter = 0
        for zoneLine in data:
            if eval(zoneLine[3])[0] <= X and \
            eval(zoneLine[4])[0] >= X and \
            eval(zoneLine[3])[1] <= Y and \
            eval(zoneLine[4])[1] >= Y :
                if AlertArea :
                    if zoneLine[5]:
                        includeZones.append(zoneLine)
                        counter+=1

                else:
                    includeZones.append(zoneLine)
                    counter+=1

        return [counter,includeZones]

class block:
    from setting import areas
    from math import floor
    
    def oneBlockSize(areaID):
        area = block.areas[areaID]
        try:
            perX = area['size'][0] / area['block'][0]
            perY = area['size'][1] / area['block'][1]
        except:
            return [-1,'no block or size info for Map']

        return [0,perX,perY]
        

    def inBlock(areaID,x,y):
        area = block.areas[areaID]

        res=block.oneBlockSize(areaID)
        if res[0] == 0:
            perX = res[1]
            perY = res[2]
        else:
            return res

        ## check input
        if x > area['size'][0] or y > area['size'][1] :
            return 'out of range'

        blockX = block.floor(x / perX) 
        blockY = block.floor(y / perY) 

        #return [perX,perY,blockX,blockY]
        return [blockX,blockY]

    def getBlockPos(areaID,x,y):
        area = block.areas[areaID]
        ## process X
        perX = area['size'][0] / area['block'][0]
        perY = area['size'][1] / area['block'][1]

        LT = [ perX * x , perY * y ]
        RB = [ perX * ( x+1 ) , perY * ( y+1 ) ]

        return [LT,RB]

class navi:
    from setting import blockMap
    findRoutes = []

    def go(areaID, start, end):
        maze = navi.blockMap[areaID]
        newMaze = []
        for idx1,val1 in enumerate(maze[0]):
            line = []
            for idx2,val2 in enumerate(maze):
                line.append(maze[idx2][idx1])
            newMaze.append(line)
        navi.visit(newMaze, start, end)
    
    def visit(maze, pt, end, route = None):
        if route == None:
            route = []

        if navi.isVisitable(maze, pt, route):
            route.append(pt)
            if navi.isEnd(route, end):
                navi.addRoute(route)
            else:
                navi.visit(maze, [pt[0], pt[1] + 1], end, route)
                navi.visit(maze, [pt[0] + 1, pt[1]], end, route)
                navi.visit(maze, [pt[0], pt[1] - 1], end, route)
                navi.visit(maze, [pt[0] - 1, pt[1]], end, route)
            route.pop()
    
    def isVisitable(maze, pt, route):
        try:
            return maze[pt[0]][pt[1]] == 1 and pt not in route
        except:
            return False
        
    def isEnd(route, end):
            return end in route

    def addRoute(route):
        navi.findRoutes.append(eval(str(route)))
        return True

    def getShortest():
        bestRoute = None
        bestRouting = 0
        for route in navi.findRoutes:
            if bestRoute == None or len(route) < bestRouting:
                bestRoute = route
                bestRouting = len(route)
        return bestRoute

