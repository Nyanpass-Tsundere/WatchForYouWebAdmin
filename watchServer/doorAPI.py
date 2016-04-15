from flask import Blueprint, request
import json
from watchDB import watchSession

doorAPI = Blueprint('doorAPI', __name__,
                        template_folder='templates')

@doorAPI.route('/')
def show():
    return 'door API here'

@doorAPI.route('/check',methods=['POST'])
def check():
    MapID = request.form.get('MapID')
    if ( MapID == None ):
        return json.dumps([-2,'no MapID']),400
    else:
        MapID = int(MapID)
    
    zone = request.form.get('zone')
    if ( zone == None ):
        return json.dumps([-2,'no zone']),400

    session = request.form.get('session')
    if ( session == None ):
        return json.dumps([-2,'no session']),400

    sessions = watchSession.list()

    tarSession = []
    for ses in sessions:
        if (ses[1] == session):
            tarSession=ses
            break

    if (tarSession == []):
        return json.dumps([-1,'fake session'])

    allowZone = json.loads(tarSession[3])
    opendoor = False
    for zoneStr in allowZone:
        thisZone = json.loads(zoneStr)
        if ( thisZone[0] == MapID and thisZone[1] == zone ):
            opendoor = True

    if (opendoor == True):
        return json.dumps([1,'open the door'])
    else:
        return json.dumps([0,'not open the door'])

    return json.dumps(zone)

