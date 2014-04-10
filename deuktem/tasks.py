# -*- coding: utf-8 -*-

from celery.decorators import periodic_task
from celery.schedules import crontab
from datetime import timedelta
from deuktem.ext import db, celery


# @periodic_task(crontab(hour=0, minute=0))
@periodic_task(run_every=timedelta(seconds=3))
def win():
    print 'Hello'

