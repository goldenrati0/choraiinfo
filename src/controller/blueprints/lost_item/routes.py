from flask import Blueprint, render_template, request

from .lost_item_crud import *

lostitem_blueprint = Blueprint("lostitembp", __name__, static_folder="../../../static",
                               template_folder="../../../templates")


@lostitem_blueprint.route("/select")
def select_item():
    return render_template("select_item.html")


@lostitem_blueprint.route("/search/vehicle", methods=["GET", "POST"])
def search_vehicle():
    if request.method == "GET":
        return render_template("search_vehicle.html")
    if request.method == "POST":
        string = request.form.get("string")
        sh = add_search_history_vehicle(string)
        print(sh.json)
        return render_template("show_vehicle.html", items=sh.matched_items())
