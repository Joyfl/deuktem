from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.assets import Environment, Bundle
from celery import Celery


db = SQLAlchemy()
login_manager = LoginManager()
celery = Celery()


def init_db(app):
    db.init_app(app)


def init_login_manager(app):
    login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    from deuktem.models import User
    return User.query.filter(User.id == id).first()


def init_assets(app):
    assets = Environment(app)
    assets.register('css_lib', Bundle(
        'bower_components/bootstrap/dist/css/bootstrap.min.css',
        filters='cssmin',
        output='../../static/css/lib.css'
    ))
    assets.register('css_dist', Bundle(
        'less/common.less',
        'less/login.less',
        'less/item.less',
        filters='less, cssmin',
        output='../../static/css/dist.css'
    ))
    assets.register('js_lib', Bundle(
        'bower_components/jquery/dist/jquery.min.js',
        'bower_components/bootstrap/dist/js/bootstrap.min.js',
        filters='jsmin',
        output='../../static/js/lib.js'
    ))
    assets.register('js_dist', Bundle(
        'coffee/common.coffee',
        'coffee/login.coffee',
        'coffee/item.coffee',
        filters='coffeescript, jsmin',
        output='../../static/js/dist.js'
    ))
    return assets


def init_celery(app):
    celery.main = app.import_name
    celery.conf.update(app.config)

