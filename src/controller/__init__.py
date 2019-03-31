from src.setup import app

from src.controller.blueprints.user import user_blueprint

app.register_blueprint(user_blueprint, url_prefix="/user")