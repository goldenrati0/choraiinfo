from flask import render_template

from src.controller import app
from src.setup import db


@app.before_first_request
def create_db():
    db.create_all()


@app.route("/")
def home():
    return render_template("main.html")


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
