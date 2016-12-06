import flask_login as login
from flask_openid import OpenID

from app.views import app
# Initialize flask-login

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        return '<User %r>' % (self.nickname)

def init_login(app):
    login_manager = login.LoginManager()
    login_manager.init_app(app)
    login_manager
    oid = OpenID(app, os.path.join(basedir, 'tmp'))

    @login_manager.user_loader
    def load_user(user_id):
        if User.is_active(user_id):
            return User.get(user_id)

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
            return redirect(somewhere)
