# -*- coding: utf8 -*-

from .blueprint import blueprint
from flask import render_template, request, current_app, redirect, url_for
from flask.ext.login import login_required
from wand.image import Image
from deuktem.models import Item
from deuktem.ext import db
import os


@blueprint.route('/')
@blueprint.route('/items')
@login_required
def item_list():
    query = Item.query
    items = query.filter(Item.winner_id == None).order_by(Item.id.desc()).all()
    return render_template('item_list.html', items=items)


@blueprint.route('/wins')
@login_required
def win_list():
    query = Item.query
    items = query.filter(Item.winner_id != 0).order_by(Item.id.desc()).all()
    return render_template('win_list.html', items=items)


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

        with Image(file=photo) as img:
            filename = 'item_%d.png' % item.id
            path = os.path.join(current_app.root_path,
                                '../../var/upload',
                                filename)

            # resize image
            size = current_app.config['PHOTO_MAX_RESOLUTION']
            if img.width > size or img.height > size:
                if img.width > img.height:
                    width = size
                    height = int(size * 1.0 * img.height / img.width)
                elif img.width < img.height:
                    height = size
                    width = int(size * 1.0 * img.width / img.height)
                else:
                    width = size
                    height = size
                img.resize(width=width, height=height)

            # save
            img.save(filename=path)
            item.photo_filename = filename
            db.session.commit()

        return redirect(url_for('web.item_list'))
