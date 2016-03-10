from flask import Blueprint, abort, request

import time

watchAPI = Blueprint('watchAPI', __name__,
                        template_folder='templates')

savepath="../uploads/"

@watchAPI.route('/')
def show():
    return 'hello world'

@watchAPI.route('/upload',methods=['GET','POST'])
def upload():
    watchID=""
    watchScanned=""

    try:
        watchID=request.form.get('ID')
        watchScanned=request.form.get('Beacons')
    except:
        return "輸入不完整！！miss some fieled"
    
    filename=time.strftime("%Y-%m-%d_%H%M%S")+".txt"

    try:
        outputfile = open(savepath+filename,"w")
        outputfile.write("get data: \n")
        outputfile.write("ID=" + str(watchID) + "\n")
        outputfile.write("BCs=" + str(watchScanned) + "\n")
        outputfile.close()
        return "sucessful save to " + savepath + filename + "ID=" + watchID ;
    except:
        return "writing failed";

        
