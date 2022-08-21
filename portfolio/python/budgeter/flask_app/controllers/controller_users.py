from flask_app import app, bcrypt
from flask import request, redirect, session

# This imports model file
from flask_app.models import model_user
# ---------- CREATE ---------- #

# ---------- READ ---------- #
# Display Route

@app.route("/user/login", methods=["POST"])
def user_new():

    model_user.User.validate_login(request.form)
    # save to session
    return redirect("/shows") ######


@app.route("/user/create", methods=["POST"])
def user_create():
    # validate
    if not model_user.User.validate_user(request.form):
        return redirect("/")


    # hash password
    hash_pw = bcrypt.generate_password_hash(request.form["password"])
    data = {
        **request.form,
        "password": hash_pw
    }

    # create user
    id = model_user.User.create(data)

    # store user in session
    session["uuid"] = id
    return redirect("/shows")


@app.route("/user/logout")
def logout_user():
    del session["uuid"]
    return redirect("/")

