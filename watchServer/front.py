#from watchServer import site
from flask import Blueprint,render_template

front = Blueprint('front',__name__,
			 template_folder='templates')

@front.route('/')
def index():
    return render_template('index.html')

@front.route('/zone')
def zone():
    return render_template('zone.html')

@front.route('/login/')
def login():
    return render_template('login.html')

@front.route('/watch')
def watch():
    return render_template('watch.html')

@front.route('/block')
def block():
    return render_template('block.html')
