from flask import Blueprint, render_template, abort

apis = Blueprint('apis', __name__,
                        template_folder='templates')

@apis.route('/')
def show():
    return 'hello world'
