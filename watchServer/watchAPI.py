from flask import Blueprint, abort, request
from watchDB import watchSession, watch

import time, json
from random import randrange 

watchAPI = Blueprint('watchAPI', __name__,
                        template_folder='templates')

savepath="../uploads/"

@watchAPI.route('/')
def show():
    return 'Watch Relate API Here'

@watchAPI.route('/fetch/<ID>')
def fetchID(ID):
    return json.dumps(watch.fetch(ID));

@watchAPI.route('/reg/<ID>')
def regWatch(ID):
    name = "手錶" + str(randrange(1,99))
    return json.dumps(watch.register(ID,name))

@watchAPI.route('/upload',methods=['POST'])
def upload():
    watchID=""
    watchScanned=""

    watchID=request.form.get('ID')
    beacons=request.form.get('Beacons')

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
    
    return json.dumps(watch.sent(watchID,filename,'not avaliable',json.dumps(fullBeacons)))
    
@watchAPI.route('/upload_xy',methods=['POST'])
def upload_xy():
    watchID=""
    watchScanned=""
    watchX=''
    watchY=''

    watchID=request.form.get('ID')
    watchScanned=request.form.get('Beacons')
    watchX=request.form.get('X')
    watchY=request.form.get('Y')
    
    try:
        session = watch.fetch(watchID)
    except:
        return json.dumps([-1,"no watchID Input!!"])

    if session[0] == 0:
        filename = watch.noSessionFile
    else :
        filename = session[2]
    ##filename=time.strftime("%Y-%m-%d_%H%M%S")+".txt"
    
    return json.dumps(watch.sent(watchID,filename,[watchX,watchY],watchScanned))
    
