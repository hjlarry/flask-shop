from flask import Blueprint, render_template

blueprint = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@blueprint.route("/")
def index():
    return render_template("dashboard/index.html")

