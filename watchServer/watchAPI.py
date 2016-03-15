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
        filename = 'notInSession'
    else :
        filename = session[2]
    ##filename=time.strftime("%Y-%m-%d_%H%M%S")+".txt"
    
    return json.dumps(watch.sent(watchID,filename,'not avaliable',watchScanned))
    
    """
    try:
        outputfile = open(savepath+filename,"w")
        outputfile.write("get data: \n")
        outputfile.write("ID=" + str(watchID) + "\n")
        outputfile.write("BCs=" + str(watchScanned) + "\n")
        outputfile.close()
        return "sucessful save to " + savepath + filename + "ID=" + watchID ;
    except:
        return "writing failed";
    """ 
