# -*- coding: utf-8 -*-
# watchServer init file 
# some debug code of server like update/restart code

from flask import Flask
app = Flask(__name__)

import watchServer.index
