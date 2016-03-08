from flask import Blueprint, abort
import json

watchAPI = Blueprint('watchAPI', __name__,
                        template_folder='templates')

@watchAPI.route('/')
def show():
    return 'hello world'

@watchAPI.route('/watchs')
def getWatchs():
    watchs = ['手錶1','手錶2','手錶3','手錶4']
    return json.dumps(watchs)

@watchAPI.route('/areas')
def getAreas():
    watchs = ['1F','2F','3F']
    return json.dumps(watchs)
