from src.controller.blueprints.lost_item import lostitem_blueprint
from src.controller.blueprints.user import user_blueprint
from src.setup import app

app.register_blueprint(user_blueprint, url_prefix="/user")
app.register_blueprint(lostitem_blueprint, url_prefix="/item")
