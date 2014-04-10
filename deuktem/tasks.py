# -*- coding: utf-8 -*-

from celery.decorators import periodic_task
from celery.schedules import crontab
from datetime import datetime
from datetime import timedelta
from deuktem.ext import db, celery  # celery beat scheduler uses `celery`
from deuktem.app import create_app
from deuktem.models import Item
import random

celery  # to remove PEP error (not used error)


@periodic_task(crontab(hour=0, minute=0))
def win():
    app = create_app()
    with app.app_context():
        items = Item.query.all()
        for item in items:
            if not item.winner and item.due.date() == datetime.now().date():
                if item.wishers.count():
                    item.winner = random.choice(item.wishers.all())
                    print "Winner of item %d is user %d" %\
                          (item.id, item.winner.id)
                else:
                    item.due = item.due.date() + timedelta(days=1)
                    print "There is no wisher for item %d. Next due: %s" %\
                          (item.id, item.due.strftime('%m/%d'))
                db.session.commit()


