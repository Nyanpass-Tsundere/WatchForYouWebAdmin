#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 0muMDAU Server
from watchServer import app 
import logging, setting
from watchServer.index import index
from werkzeug.contrib.fixers import ProxyFix 

# muMDAU_app setting 
app.secret_key = setting.yourkey
app.wsgi_app = ProxyFix(app.wsgi_app)

# Main function of MDAUServer
if __name__ == '__main__':
    # log writeing
    logging.basicConfig(filename=setting.s_log, level=logging.DEBUG)
    print('Server Run on ' + str(setting.host) + ':' + str(setting.port))
    # check debug
    if setting.debug == 0:
        debugB = False 
    else:
        debugB = True
        print('Debug Mode is run!')
    app.run(host=str(setting.host), port=setting.port, debug=debugB)
