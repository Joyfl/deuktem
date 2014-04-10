from .blueprint import blueprint
from flask import render_template


@blueprint.errorhandler(401)
def need_login(e):
    return render_template('login.html')
