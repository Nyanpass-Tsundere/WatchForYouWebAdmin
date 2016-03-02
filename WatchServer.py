#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 0muMDAU Server
from watchServer import site
import logging, setting
from werkzeug.contrib.fixers import ProxyFix 

# muMDAU_app setting 
site.secret_key = setting.yourkey
site.wsgi_app = ProxyFix(site.wsgi_app)

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
    site.run(host=str(setting.host), port=setting.port, debug=debugB)
