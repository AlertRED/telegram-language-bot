from flask import Flask
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView

from database.access import Session
from database.models import User, Collection, Folder, Term


class BaseView(ModelView):
    can_edit = True
    can_delete = True
    can_create = True
    can_view_details = True


def create_app() -> Flask:
    app = Flask(__name__)
    app.config['FLASK_ADMIN_SWATCH'] = 'cosmo'
    app.secret_key = 'key'

    admin = Admin(
        app,
        name='AdminPanel',
        index_view=AdminIndexView(name='Home', url='/'),
        template_mode='bootstrap4',
    )
    session = Session()
    admin.add_view(BaseView(User, session, name='User'))
    admin.add_view(BaseView(Collection, session, name='Collection'))
    admin.add_view(BaseView(Folder, session, name='Folder'))
    admin.add_view(BaseView(Term, session, name='Term'))
    return admin.app


if __name__ == '__main__':
    app = create_app()
    app.run()
