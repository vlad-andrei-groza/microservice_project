from flask import Blueprint, render_template


web_bp = Blueprint("web", __name__)


@web_bp.route("/")
def index():
    return render_template("base.html")


# create a route for the login page
@web_bp.route("/login")
def login():
    return render_template("login.html")
