from flask import Blueprint, abort, request
import json
from watchDB import watchManager, watchSession, zone, watch
from setting import areas, blockMap

webAPI = Blueprint('webAPI', __name__,
                        template_folder='templates')

@webAPI.route('/')
def show():
    return 'web API here'

@webAPI.route('/maps')
def getAreas():
    return json.dumps(areas)

@webAPI.route('/watch/list')
def getWatchs():
    fullData = []
    for watch in watchManager.watchs():
        name = watchManager.getName(watch)
        fullData.append( {'name': name, 'ID': watch} )
    return json.dumps(fullData)

@webAPI.route('/watch/list/act')
def getActWatchs():
    fullData = []
    for watch in watchManager.actWatchs():
        name = watchManager.getName(watch)
        fullData.append( {'name': name, 'ID': watch} )
    return json.dumps(fullData)

@webAPI.route('/watch/Act',methods=['POST'])
def ActWatch(ID = None):
    from setting import t_format
    from datetime import datetime, timedelta

    ID = request.form.get('ID')
    if ( ID == None ):
        return json.dumps([-2,'no ID']),400

    hour = request.form.get('hour')
    if ( hour == None ):
        return json.dumps([-2,'no Hour']),400

    zoneName = request.form.get('zone')
    if ( zoneName == None ):
        return json.dumps([-2,'no zone']),400

    expTime = datetime.now() + timedelta(hours=int(hour))
    expTimeStr = format(expTime, t_format)

    return json.dumps(watchSession.new(ID,expTimeStr,zoneName))

@webAPI.route('/watch/Name',methods=['POST'])
def nameWatch():
    ID = request.form.get('ID')
    if ( ID == None ):
        return json.dumps([-2,'no ID']),400

    Name = request.form.get('Name')
    if ( Name == None ):
        return json.dumps([-2,'no Name']),400

    return json.dumps(watch.naming(ID,Name))

@webAPI.route('/watch/loc/<ID>')
@webAPI.route('/watch/loc/<ID>/<NUMBER>')
def locs(ID,NUMBER=1):
    return json.dumps(watchManager.getPos(ID,NUMBER))

@webAPI.route('/zone/list/<mapID>')
def listZone(mapID):
    return json.dumps(zone.listZone(mapID))

@webAPI.route('/zone/new',methods=['POST'])
def newZone():
    MapID = request.form.get('MapID')
    zoneName = request.form.get('Name')
    LT = request.form.get('LT')
    RB = request.form.get('RB')

    x1 = eval(LT)[0]
    y1 = eval(LT)[1]
    x2 = eval(RB)[0]
    y2 = eval(RB)[1]

    if ( x1 > x2 or y1 > y2 or len(zoneName) < 2 ):
        return json.dumps([-2,'Data wrong!!']), 400
    else:
        dbOP = zone.newZone(MapID,zoneName,LT,RB)
        if dbOP[0] >= 0:
            return json.dumps(dbOP), 200
        else:
            return json.dumps(dbOP), 500

@webAPI.route('/zone/rename',methods=['POST'])
def renameZone():
    MapID = request.form.get('MapID')
    zoneName = request.form.get('Name')
    zoneNewName = request.form.get('NewName')

    dbOP = zone.renameZone(MapID,zoneName,zoneNewName)
    if dbOP[0] >= 0:
        return json.dumps(dbOP), 200
    else:
        return json.dumps(dbOP), 500

@webAPI.route('/zone/setAlert',methods=['POST'])
def setAlertZone():
    MapID = request.form.get('MapID')
    zoneName = request.form.get('Name')
    zoneAlert = request.form.get('Alert')

    dbOP = zone.setAlertZone(MapID,zoneName,zoneAlert)
    if dbOP[0] >= 0:
        return json.dumps(dbOP), 200
    else:
        return json.dumps(dbOP), 500

@webAPI.route('/zone/del',methods=['POST'])
def delZone():
    MapID = request.form.get('MapID')
    zoneName = request.form.get('Name')

    dbOP = zone.delZone(MapID,zoneName)
    if dbOP[0] >= 0:
        return json.dumps(dbOP), 200
    else:
        return json.dumps(dbOP), 500

@webAPI.route('/block/<MapID>')
def getblockMap(MapID):
    return json.dumps(blockMap[int(MapID)])

@webAPI.route('/alert/new')
def getNewAlert():
    from tail import tail
    from setting import alert_log, t_format
    from datetime import datetime, timedelta

    alertLog = tail(alert_log,30,[0,1,2,3])

    nearTime = datetime.now() - timedelta(minutes=30)
    nearTimeStr = format(nearTime, t_format)
    print(nearTimeStr)

    nearAlert = []
    for alert in alertLog:
        if alert[0] > nearTimeStr:
            nearAlert.append(alert)


    return json.dumps(nearAlert)

@webAPI.route('/alert/<num>')
def getAlert(num):
    from tail import tail
    from setting import alert_log

    alertLog = tail(alert_log,num,[0,1,2,3])
    return json.dumps(alertLog)
