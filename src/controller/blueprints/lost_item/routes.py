from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from .lost_item_crud import *

lostitem_blueprint = Blueprint("lostitembp", __name__, static_folder="../../../static",
                               template_folder="../../../templates")


@lostitem_blueprint.route("/select")
def select_item():
    return render_template("select_item.html")


@lostitem_blueprint.route("/report/vehicle", methods=["GET", "POST"])
@login_required
def report_vehicle():
    if request.method == "GET":
        return render_template("add_vehicle.html")
    if request.method == "POST":
        print(request.form)
        license = request.form.get("license")
        serial = request.form.get("serial")
        engine = request.form.get("engine")
        remarks = request.form.get("remarks")
        stolen = request.form.get("stolen") == "1"
        print(stolen)

        item = add_item(current_user.uid, ItemTypeEnum.VEHICLE, serial_number=serial, engine_number=engine,
                        license_number=license, remarks=remarks, is_stolen=stolen)
        return redirect(url_for("userbp.dashboard"))


@lostitem_blueprint.route("/report/laptop", methods=["GET", "POST"])
@login_required
def report_laptop():
    if request.method == "GET":
        return render_template("add_laptop.html")
    if request.method == "POST":
        license = request.form.get("license")
        serial = request.form.get("serial")
        engine = request.form.get("engine")
        remarks = request.form.get("remarks")

        item = add_item(current_user.uid, ItemTypeEnum.VEHICLE, serial_number=serial, engine_number=engine,
                        license_number=license)
        return redirect(url_for("userbp.dashboard"))


@lostitem_blueprint.route("/report/mobile", methods=["GET", "POST"])
@login_required
def report_mobile():
    if request.method == "GET":
        return render_template("add_mobile.html")
    if request.method == "POST":
        license = request.form.get("license")
        serial = request.form.get("serial")
        engine = request.form.get("engine")
        remarks = request.form.get("remarks")

        item = add_item(current_user.uid, ItemTypeEnum.VEHICLE, serial_number=serial, engine_number=engine,
                        license_number=license)
        return redirect(url_for("userbp.dashboard"))


@lostitem_blueprint.route("/search/vehicle", methods=["GET", "POST"])
def search_vehicle():
    if request.method == "GET":
        return render_template("search_vehicle.html")
    if request.method == "POST":
        string = request.form.get("string")
        sh = add_search_history_vehicle(string)
        print(sh.json)
        return render_template("show_vehicle.html", items=sh.matched_items())


@lostitem_blueprint.route("/search/laptop", methods=["GET", "POST"])
def search_laptop():
    if request.method == "GET":
        return render_template("search_laptop.html")
    if request.method == "POST":
        string = request.form.get("string")
        sh = add_search_history_laptop(string)
        print(sh.json)
        return render_template("show_laptop.html", items=sh.matched_items())


@lostitem_blueprint.route("/search/phone", methods=["GET", "POST"])
def search_phone():
    if request.method == "GET":
        return render_template("search_mobile.html")
    if request.method == "POST":
        string = request.form.get("string")
        sh = add_search_history_phone(string)
        print(sh.json)
        return render_template("show_mobile.html", items=sh.matched_items())
