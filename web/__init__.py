from flask import Flask
from flask.ext.misaka import Misaka

app = Flask(__name__)
app.config.from_object('web.config')

Misaka(app, autolink=True)

import web.hooks
import web.views
