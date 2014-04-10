import code
from deuktem.app import create_app
from deuktem.ext import db
from deuktem.models import *

app = create_app()
with app.app_context():
    code.interact(local=dict(globals(), **locals()))
