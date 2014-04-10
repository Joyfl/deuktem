# -*- coding: utf-8 -*-

import os
from flask import Flask
from deuktem.config import DefaultConfig
from deuktem import ext


def hello():
    from math import ceil
    line_length = 80
    hello = 'Deuktem'
    left = (line_length - len(hello)) / 2 - 3
    right = int(ceil((line_length - len(hello)) / 2.0) - 3)
    line = '#' * line_length
    print line
    print '#', ' ' * left, hello, ' ' * right, '#'
    print line
hello()


def create_app(config=None):
    if not config:
        config = DefaultConfig()

    app = Flask(__name__)

    app.config.from_object(config)
    import_modules(app)
    init_extensions(app)

    return app


def init_extensions(app):
    ext.init_db(app)
    ext.init_login_manager(app)
    ext.init_assets(app)
    ext.init_celery(app)


def import_modules(app):
    """Register blueprints from `modules` package.
    """
    try:
        modules = os.listdir(os.path.join(app.root_path, 'modules'))
    except OSError:
        app.logger.info('modules directory not found.')
        return

    for f in modules:
        path = os.path.join(app.root_path, 'modules', f)
        if os.path.isdir(path) and f[0] != '.' and f[0] != '_':
            blueprint_path = os.path.join(path, 'views', 'blueprint.py')
            if os.path.isfile(blueprint_path):
                module = __import__("deuktem.modules.%s.views.blueprint" % f,
                                    fromlist=['blueprint'])
                try:
                    blueprint = getattr(module, 'blueprint')
                    app.register_blueprint(blueprint)
                    app.logger.info('* Registered module: ' + f)
                except:
                    pass
