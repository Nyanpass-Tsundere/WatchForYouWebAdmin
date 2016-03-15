from flask import Blueprint, abort
import json
from watchDB import watchManager, watchSession

webAPI = Blueprint('webAPI', __name__,
                        template_folder='templates')

@webAPI.route('/')
def show():
    return 'hello world'

@webAPI.route('/areas')
def getAreas():
    areas = [{'name': '1F', 'ID': '0001', 'map': '/static/maps/1f.png'},
            {'name': 'LAB', 'ID': '0002', 'map': '/static/maps/LAB.png'},
            {'name': '3F', 'ID': '0003'}]
    return json.dumps(areas)

@webAPI.route('/watch/list')
def getWatchs1():
    fullData = []
    for watch in watchManager.watchs():
        name = watchManager.getName(watch)
        fullData.append( {'name': name, 'ID': watch} )
    return json.dumps(fullData)

@webAPI.route('/watch/listAct')
def getActWatchs():
    fullData = []
    for watch in watchManager.actWatchs():
        name = watchManager.getName(watch)
        fullData.append( {'name': name, 'ID': watch} )
    return json.dumps(fullData)

@webAPI.route('/watch/Act/<ID>')
def ctWatch(ID):
    return json.dumps(watchSession.new(ID,"2015-06-06"))
