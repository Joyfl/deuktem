# -*- coding: utf-8 -*-


from deuktem.ext import db
from flask import current_app
from flask.ext.login import UserMixin, current_user
import datetime


def tomorrow():
    return datetime.date.today() + datetime.timedelta(days=1)


wishlist = db.Table(
    'wishlist',
    db.Column(
        'user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True
    ),
    db.Column(
        'item_id', db.Integer, db.ForeignKey('item.id'), primary_key=True
    )
)

win = db.Table(
    'win',
    db.Column(
        'user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True
    ),
    db.Column(
        'item_id', db.Integer, db.ForeignKey('item.id'), primary_key=True
    )
)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    facebook_id = db.Column(db.String(20), unique=True)
    facebook_token = db.Column(db.String(255), unique=True)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    photo_filename = db.Column(db.String(40))
    name = db.Column(db.String(40), nullable=False)
    description = db.Column(db.Text)
    due = db.Column(db.DateTime, nullable=False, default=tomorrow())
    wishers = db.relationship('User', secondary=wishlist, lazy='dynamic')
    winner = db.relationship('User')
    winner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    @property
    def url(self):
        if self.photo_filename:
            return 'http://%s/upload/%s' % (current_app.config['SERVER_NAME'],
                                            self.photo_filename)
        return 'http://%s/static/image/placeholder.jpg' % (
            current_app.config['SERVER_NAME']
        )

    @property
    def wished(self):
        return db.session.query(wishlist).filter(
            wishlist.c.user_id == current_user.id
        ).filter(
            wishlist.c.item_id == self.id
        ).count() != 0

