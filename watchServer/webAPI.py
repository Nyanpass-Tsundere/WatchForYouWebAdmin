from flask import Blueprint, abort
import json
from watchDB import watchManager, watchSession, zone
from setting import areas

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

@webAPI.route('/watch/Act/<ID>')
def ctWatch(ID):
    return json.dumps(watchSession.new(ID,"2016-06-06"))

@webAPI.route('/watch/loc/<ID>')
@webAPI.route('/watch/loc/<ID>/<NUMBER>')

def locs(ID,NUMBER=1):
    return json.dumps(watchManager.getPos(ID,NUMBER))

@webAPI.route('/zone/list/<mapID>')
def listZone(mapID):
    return json.dumps(zone.listZone(mapID))
