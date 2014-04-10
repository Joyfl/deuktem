# -*- coding: utf-8 -*-

from flask import Response
from werkzeug import LocalProxy
from functools import wraps
from deuktem.ext import db
import json


def json_response(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        data = f(*args, **kwargs)
        status = 0

        if data is None:
            data = {}

        elif isinstance(data, tuple):
            status = data[1]
            data = data[0]

        elif isinstance(data, LocalProxy):
            data = data._get_current_object()

        if isinstance(data, Response):
            return data

        elif isinstance(data, list):
            if len(data) and isinstance(data[0], db.Model):
                data = {'data': [elem.serialize() for elem in data]}
            else:
                data = {'data': data}

        elif isinstance(data, db.Model):
            data = data.serialize()

        return Response(json.dumps(data), mimetype='application/json',
                        status=status or 200)
    return decorator


def cors(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        response = f(*args, **kwargs)
        response.headers['Access-Control-Allow-Origin'] = '*'
        print response.headers
        return response
    return decorator


class classproperty(object):
    def __init__(self, getter):
        self.getter = classmethod(getter)

    def __get__(self, *arg):
        return self.getter.__get__(*arg)()
