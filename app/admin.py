from app.views import app
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.fileadmin import FileAdmin
import os.path as op


class MyView(BaseView):
    def is_accessible(self):
        return True  # login.current_user.is_authenticated()

    @expose('/')
    def index(self):
            return self.render('adminIndex.html')


admin = Admin(app)
admin.add_view(MyView(name='Hello'))
path = op.join(op.dirname(__file__), 'static')
admin.add_view(FileAdmin(path, '/static/', name='Static Files'))

