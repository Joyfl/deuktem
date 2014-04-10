# -*- coding: utf8 -*-

from .blueprint import blueprint
from flask.ext.login import login_required, current_user
from deuktem.models import Item
from deuktem.ext import db
from deuktem.decorators import json_response


@blueprint.route('/items/<int:id>/wish', methods=('POST',))
@login_required
@json_response
def item_wish_new(id):
    item = Item.query.get_or_404(id)
    item.wishers.append(current_user)
    try:
        db.session.commit()
    except:
        db.session.rollback()
        return {}, 400
    return {
        'id': current_user.id,
        'name': current_user.name
    }


@blueprint.route('/items/<int:id>/wish', methods=('DELETE',))
@login_required
@json_response
def item_wish_delete(id):
    item = Item.query.get_or_404(id)
    item.wishers.remove(current_user)
    try:
        db.session.commit()
    except:
        db.session.rollback()
        return {}, 400
    return {
        'id': current_user.id,
        'name': current_user.name
    }
