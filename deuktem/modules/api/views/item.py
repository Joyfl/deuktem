# -*- coding: utf8 -*-

from .blueprint import blueprint
from flask import request, current_app
from deuktem.models import Item
from deuktem.ext import db
from deuktem.decorators import json_response, cors
import os


@blueprint.route('/items', methods=('POST',))
@cors
@json_response
def item_new():
    photo = request.files.get('photo')
    name = request.forms.get('name')
    description = request.forms.get('description')

    item = Item()
    item.name = name
    item.description = description

    db.session.add(item)
    db.session.commit()

    if photo:
        filename = 'item_%d.png' % item.id
        path = os.path.join(current_app.root_path,
                            '../../var/upload',
                            filename)
        photo.save(path)
        item.filename = filename
        db.session.commit()

    return {}, 201
