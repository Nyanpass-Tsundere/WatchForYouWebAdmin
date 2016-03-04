# -*- coding: utf-8 -*-
# watchServer init file 
# some debug code of server like update/restart code

from flask import Flask
from watchServer.front import front
from watchServer.apis import apis

site = Flask(__name__)

#import watchServer.index
site.register_blueprint(front)
site.register_blueprint(apis,url_prefix='/api_web')
