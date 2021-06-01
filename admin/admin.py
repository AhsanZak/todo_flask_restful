from flask import Blueprint, render_template
from flask import Flask

app = Flask(__name__)
dashboard = Blueprint("dashboard", __name__, static_folder="static", template_folder="templates")

@dashboard.route("/admin")
@dashboard.route("/")
def adminpanel():
    return render_template("indexAdmin.html")