# -*- coding: utf-8 -*-

from .blueprint import blueprint
from flask import request, render_template, flash, redirect, url_for
from flask.ext.login import login_user, logout_user
from deuktem.models import User
from deuktem.ext import db
import facebook


@blueprint.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'GET':
        return render_template('login.html')

    facebook_id = request.form.get('facebook_id')
    facebook_token = request.form.get('facebook_token')

    if not facebook_id or not facebook_token:
        flash(u"잘못된 로그인 정보입니다.")
        return render_template('login.html'), 400

    me = facebook_auth(facebook_token)
    if not me:
        flash(u"페이스북 인증에 실패했습니다.")
        return render_template('login.html'), 400

    user = User.query.filter_by(facebook_id=str(me['id'])).first()
    if user is None:
        user = User()
        user.name = me['name']
        user.facebook_id = facebook_id
        user.facebook_token = facebook_token
        db.session.add(user)
        db.session.commit()

    login_user(user)
    return redirect(url_for('web.item_list'))


@blueprint.route('/logout', methods=('GET', 'POST'))
def logout():
    logout_user()
    return redirect(url_for('web.login'))


def facebook_auth(token, fields='id,name'):
    graph = facebook.GraphAPI(token)
    try:
        me = graph.get_object('me', fields=fields)
    except facebook.GraphAPIError:
        return False
    return me
