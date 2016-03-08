from flask import Blueprint, abort
import json

webAPI = Blueprint('webAPI', __name__,
                        template_folder='templates')

@webAPI.route('/')
def show():
    return 'hello world'

@webAPI.route('/watchs')
def getWatchs():
    watchs = [{'name': '手錶1', 'ID': '0001'},{'name': '手錶2', 'ID': '0002'},{'name': '手錶三', 'ID': '0003'}]
    return json.dumps(watchs)

@webAPI.route('/areas')
def getAreas():
    areas = [{'name': '1F', 'ID': '0001', 'map': '/static/maps/1f.png'},
            {'name': 'LAB', 'ID': '0002', 'map': '/static/maps/LAB.png'},
            {'name': '3F', 'ID': '0003'}]
    return json.dumps(areas)
