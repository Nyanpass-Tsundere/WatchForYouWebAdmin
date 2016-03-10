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
        watchScanned=request.form.get('status')
    except:
        try:
            watchID=request.args.get('ID')
            watchScanned=request.args.get('status')
        except:
            return "輸入不完整！！miss some fieled"
    
    filename=time.strftime("%Y-%m-%d_%H%M%S")+".txt"

    try:
        outputfile = open(savepath+filename,"w")
        outputfile.write("get data: \n")
        outputfile.write(str(watchID) + "\n")
        outputfile.write(str(watchScanned) + "\n")
        return "sucessful save to " + savepath + filename;
    except:
        return "writing failed";

        
