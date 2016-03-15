from flask import Blueprint, abort, request
from watchDB import watchSession, watch

import time, json
from random import randrange 

watchAPI = Blueprint('watchAPI', __name__,
                        template_folder='templates')

savepath="../uploads/"

@watchAPI.route('/')
def show():
    return 'hello world'

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

    try:
        watchID=request.form.get('ID')
        watchScanned=request.form.get('Beacons')
    except:
        return "輸入不完整！！miss some fieled"
    
    session = watch.fetch(watchID)
    if session[0] == 0:
        filename = watch.noSessionFile
    else :
        filename = session[2]
    ##filename=time.strftime("%Y-%m-%d_%H%M%S")+".txt"
    
    return json.dumps(watch.sent(watchID,filename,'not avaliable',watchScanned))
    
@watchAPI.route('/upload_xy',methods=['POST'])
def upload_xy():
    watchID=""
    watchScanned=""
    watchX=''
    watchY=''

    try:
        watchID=request.form.get('ID')
        watchScanned=request.form.get('Beacons')
        watchX=request.form.get('X')
        watchY=request.form.get('Y')


    except:
        return "輸入不完整！！miss some fieled"
    
    session = watch.fetch(watchID)
    if session[0] == 0:
        filename = watch.noSessionFile
    else :
        filename = session[2]
    ##filename=time.strftime("%Y-%m-%d_%H%M%S")+".txt"
    
    return json.dumps(watch.sent(watchID,filename,[watchX,watchY],watchScanned))
    
