from flask import Blueprint, render_template

mod = Blueprint('site', __name__, template_folder='templates', static_folder='static')


@mod.route('/')
def index():
    return render_template('index.html')
