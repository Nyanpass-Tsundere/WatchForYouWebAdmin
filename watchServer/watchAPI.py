from flask import Blueprint, abort, request
from watchDB import watchSession, watch, watchManager, block, zone


import time, json
from random import randrange 

watchAPI = Blueprint('watchAPI', __name__,
                        template_folder='templates')

savepath="../uploads/"

@watchAPI.route('/')
def show():
    return 'Watch Relate API Here'

@watchAPI.route('/fetch/<ID>')
@watchAPI.route('/fetch',methods=['POST'])
def fetchID(ID=None):
    if request.method == 'POST':
        ID=request.form.get('ID')
    if ID == None:
        return json.dumps([-2,'no ID'])
    return json.dumps(watch.fetch(ID,forWatch = True));

@watchAPI.route('/reg/<ID>')
@watchAPI.route('/reg',methods=['POST'])
def regWatch(ID=None):
    if request.method == 'POST':
        ID=request.form.get('ID')
    if ID == None:
        return json.dumps([-2,'no ID'])
    name = "手錶" + str(randrange(1,99))
    return json.dumps(watch.register(ID,name))

@watchAPI.route('/upload',methods=['POST'])
def upload():
    from position import resLocate
    from operator import itemgetter
    from setting import beaconsMap
    
    watchID=""
    watchScanned=""

    watchID=request.form.get('ID')
    beacons=request.form.get('Beacons')
    moving=request.form.get('Move')

    try:
        fullBeacons = []
        for beacon in beacons.replace('[','').replace(']','').replace('},{','}},{{').split('},{'):
            info = beacon.replace('{','').replace('}','').split(',')
            formatedInfo = {'macAddress' : info[0].replace('macAddress:','') ,
                    info[1].split(':')[0] : info[1].split(':')[1], 
                    info[2].split(':')[0] : int(info[2].split(':')[1]), 
                    info[3].split(':')[0] : int(info[3].split(':')[1]), 
                    info[4].split(':')[0] : int(info[4].split(':')[1]),
                    info[5].split(':')[0] : int(info[5].split(':')[1])
                    }
            fullBeacons.append(formatedInfo)
    except:
        return json.dumps([-3,"beacon info type wrong"])
    
    try:
        session = watch.fetch(watchID)
    except:
        return json.dumps([-1,"no watchID Input!!"])

    if session[0] == 0:
        filename = watch.noSessionFile
    else :
        filename = session[2]
    ##filename=time.strftime("%Y-%m-%d_%H%M%S")+".txt"

    ## convert RSSI to value that can react distance ratio
    ## ref: http://stackoverflow.com/questions/20416218/understanding-ibeacon-distancing/20434019#20434019
    for beacon in fullBeacons:
        ratio = beacon['rssi'] / beacon['measuredPower']
        #if ( ratio < 1.0 ):
        #    beacon['DIST'] = pow(ratio,10);
        #else:
        #    beacon['DIST'] = (0.89976)*pow(ratio,7.7095) + 0.111;
        beacon['DIST'] = (0.89976)*pow(ratio,7.7095) + 0.111;
        ## lookup beacon locates
        try:
            beacon['MapID'] = beaconsMap[beacon['macAddress']][0]
            beacon['Locate'] = beaconsMap[beacon['macAddress']][1]
        except:
            beacon['MapID'] = -1
            beacon['Locate'] = ''

    orderBeacons = sorted(fullBeacons,key=itemgetter('DIST'))

    ## find user's MapID
    MapID = orderBeacons[0]['MapID']

    ## kick beacons not in same MapID
    for idx,val in enumerate(orderBeacons):
        if ( val['MapID'] != MapID  or val['MapID'] == -1 ):
            orderBeacons.pop(idx)

    ## prepare data
    beaconLocs = []
    beaconDist = []
    noEnoughtBeacons = False
    for i in [0]:
        try:
            beaconDist.append(orderBeacons[i]['DIST'])
            beaconLocs.append(orderBeacons[i]['Locate'])
        except:
            noEnoughtBeacons = True
            break
    if (noEnoughtBeacons == True):
        locate = [-1,-1,MapID]
    else:
        print(beaconLocs)
        print(beaconDist)
        res = resLocate(beaconLocs,beaconDist)
        if res == None:
            locate = [-2,-2,MapID]
        else:
            locate = [float(res[0][0]),float(res[0][1]),MapID]

    return json.dumps(watch.sent(watchID,filename,locate,json.dumps(fullBeacons),moving))
    
@watchAPI.route('/upload_xyz',methods=['POST'])
def upload_xy():
    watchID=""
    watchScanned=""
    watchX=''
    watchY=''
    ## 雖然叫做Z軸，實際上是MapID
    watchZ=''

    watchID=request.form.get('ID')
    watchScanned=request.form.get('Beacons')
    watchX=request.form.get('X')
    watchY=request.form.get('Y')
    watchZ=request.form.get('Z')
    
    try:
        session = watch.fetch(watchID)
    except:
        return json.dumps([-1,"no watchID Input!!"])

    if session[0] == 0:
        filename = watch.noSessionFile
    else :
        filename = session[2]
    ##filename=time.strftime("%Y-%m-%d_%H%M%S")+".txt"
    
    return json.dumps(watch.sent(watchID,filename,[watchX,watchY,watchZ],watchScanned))
    
@watchAPI.route('/getRoute',methods=['POST'])
def getPATH():
    from watchDB import navi
    a = navi()

    ID = request.form.get('ID')
    if ID == None:
        return json.dumps([-1,"noID"])

    fetch = json.loads(getBlock(ID))
    if fetch[0] == 0:
        loc = fetch[1]
        cur_block = fetch[2]
    
    ## search for target zone
    targetZoneMapID = request.form.get('tarMapID')
    targetZoneName = request.form.get('tarName')
    if ( targetZoneMapID == None or targetZoneName == None ):
        return json.dumps([-3,"no spec target"])
    targetZoneMapID = int(targetZoneMapID)

    zoneData = zone.listZone(targetZoneMapID)
    if ( zoneData[0] != 0 ):
        return json.dumps([-4,"no target exist"])
    zoneData = zoneData[1]

    tarZone = False
    for data in zoneData:
        if data[0] == targetZoneName:
            tarZone = data
    
    if tarZone == False:
        return json.dumps([-4,"no target exist"])

    ## if need elevator
    if targetZoneMapID != loc[2] :
        return json.dumps([-10,'need elevator'])

    ## end(door) block
    if tarZone[2] == None:
        ## Zone no Map Set
        LT = eval(tarZone[3])
        RB = eval(tarZone[4])
        center = [ (LT[0]+RB[0])/2 , (LT[1]+RB[1])/2   ]
        door = block.inBlock(targetZoneMapID,center[0],center[1]) 
    else:
        door = eval(tarZone[2])

    print([loc[2],cur_block,door])
    a.go(int(loc[2]),cur_block,door)
    route = a.getShortest()
    if route == None:
        return json.dumps([-5,"no route exist"])

    route_det = []
    for idx, step in enumerate(route):
        if step == door:
            route_det.append([step,'FINISH'])
        else:
            step_detail = [ route[idx+1][0] - step[0] , route[idx+1][1] - step[1] ]
            if ( step_detail == [0,-1] ) :
                route_det.append([step,'UP'])
            elif ( step_detail == [0,1] ) :
                route_det.append([step,'DOWN'])
            elif ( step_detail == [-1,0] ) :
                route_det.append([step,'LEFT'])
            elif ( step_detail == [1,0] ) :
                route_det.append([step,'RIGHT'])
            else:
                route_det.append([step,'routing'])

    return json.dumps([0,route_det])

@watchAPI.route('/getRouteBlock',methods=['POST'])
def getBlock(ID = None):
    if ID == None:
        ID = request.form.get('ID')
    if ID == None:
        return json.dumps([-1,"noID"])

    loc = watchManager.getPos(ID,1)
    if loc == []:
        return json.dumps([-2,"can not find your location"])
    loc = loc[0][1]
    loc[0] = float(loc[0])
    loc[1] = float(loc[1])
    loc[2] = int(loc[2])

    cur_block = block.inBlock(loc[2],loc[0],loc[1])

    return json.dumps([0,loc,cur_block])
