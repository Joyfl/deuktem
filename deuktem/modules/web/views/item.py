# -*- coding: utf8 -*-

from .blueprint import blueprint
from flask import render_template, request, current_app, redirect, url_for
from flask.ext.login import login_required
from deuktem.models import Item
from deuktem.ext import db
import os


@blueprint.route('/')
@blueprint.route('/items')
@login_required
def item_list():
    items = Item.query.order_by(Item.id.desc()).all()
    return render_template('item_list.html', items=items)


@blueprint.route('/items/new', methods=('GET', 'POST'))
@login_required
def item_new():
    if request.method == 'GET':
        return render_template('item_new.html')

    else:
        photo = request.files.get('photo')
        name = request.form.get('name')
        description = request.form.get('description')

        if not name or len(name) == 0:
            return render_template('item_new.html')

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
            item.photo_filename = filename
            db.session.commit()

        return redirect(url_for('web.item_list'))
