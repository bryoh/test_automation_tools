from flask import Flask

app = Flask(__name__)
from blue import admin
from blue import site

from blue.site.routes import mod
from blue.admin.routes import mod

app.register_blueprint(admin.routes.mod)
app.register_blueprint(site.routes.mod)
