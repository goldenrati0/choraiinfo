from flask_admin import Admin

from src.controller.blueprints.lost_item import lostitem_blueprint
from src.controller.blueprints.user import user_blueprint
from src.setup import app, db
from flask_admin.contrib.sqla import ModelView

from src.model import User, Vehicle, Laptop, CellPhone, SearchHistory

app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

admin = Admin(app, name='choraiinfo', template_mode='bootstrap3')

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Vehicle, db.session))
admin.add_view(ModelView(Laptop, db.session))
admin.add_view(ModelView(CellPhone, db.session))
admin.add_view(ModelView(SearchHistory, db.session))

app.register_blueprint(user_blueprint, url_prefix="/user")
app.register_blueprint(lostitem_blueprint, url_prefix="/item")
