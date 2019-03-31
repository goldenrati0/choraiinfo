from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager

from src.config import Configuration

app = Flask(__name__, static_folder="../static", template_folder="../templates")
CORS(app)
app.config.from_object(Configuration)
login_manager = LoginManager(app)
