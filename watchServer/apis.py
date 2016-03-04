from flask import Blueprint, render_template, abort
import json

apis = Blueprint('apis', __name__,
                        template_folder='templates')

@apis.route('/')
def show():
    return 'hello world'

@apis.route('/watchs')
def getWatchs():
    watchs = ['手錶1','手錶2','手錶3','手錶4']
    return json.dumps(watchs)

@apis.route('/areas')
def getAreas():
    watchs = ['1F','2F','3F']
    return json.dumps(watchs)
