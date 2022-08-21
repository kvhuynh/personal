from flask_app import app
from flask import render_template, redirect, session

from flask_app.models import model_user, model_user_balance

@app.route("/")
def index():
    if "uuid" in session:
        return redirect("/dashboard")
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    if "uuid" not in session:
        return redirect("/")
    context = {
        "user_first_name": model_user.User.get_one({"id":session["uuid"]}).first_name,
        "show_list": model_user_balance.Show.get_all()
    }
    if context["show_list"] == False:
        return render_template("/dashboard.html")
    return render_template("/dashboard.html", **context)

@app.route("/dashboard/breakdown")
def budget_breakdown():
    pass