from watchDB import watchSession, watchManager, zone
from time import sleep, strftime
import json
from setting import t_format, alert_log

while True:
    sessions = watchSession.list()
    
    msgs = []

    for ses in sessions:
        allowArea = json.loads(ses[3])
        watchID = ses[0]

        watchLoc = watchManager.getPos(watchID)
        if watchLoc != []:
            watchLoc = watchLoc[0][1]

            MapID = int(watchLoc[2])
            watchZone = zone.inZone(MapID,int(watchLoc[0]),int(watchLoc[1]))

            disallowZone = list(zone.listZone(watchLoc[2])[1])
            for idx,oneZone in enumerate(disallowZone):
                disallowZone[idx] = list(disallowZone[idx])
                disallowZone[idx].pop(4)
                disallowZone[idx].pop(3)
                disallowZone[idx].pop(2)
                disallowZone[idx].pop(1)

            allowIndex = []
            for idx,val in enumerate(disallowZone):
                for allow in allowArea:
                    unit = json.loads(allow)
                    forceAlert = val[1]
                    if ( unit[0] == MapID and unit[1] == val[0]):
                        if ( forceAlert == 0 ):
                            allowIndex.append(idx)
                        else:
                            disallowZone[idx].append(1)
                    else:
                        disallowZone[idx].append(0)


            allowIndex.reverse()
            for i in allowIndex:
                disallowZone.pop(i)

            #print(watchID)
            #print('not allow to')
            #print(disallowZone)
            #print('=================')

            for zoneData in watchZone[1]:
                #print('watch@')
                #print(zoneData)
                for block in disallowZone:
                    if block[0] == zoneData[0]:
                        eventTime = strftime(t_format)
                        warnMode = block[2]
                        block.pop(2)
                        msgs.append(json.dumps([eventTime,warnMode,watchID,block]))
    file = open(alert_log,'a')
    for msg in msgs:
        file.writelines(msg+"\n")
    file.close()

    print(msgs) 
    sleep(30)
