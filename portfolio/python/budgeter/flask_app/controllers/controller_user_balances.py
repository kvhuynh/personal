from flask_app import app
from flask import render_template, request, redirect, session, flash

# This imports model file
from flask_app.models import model_user, model_user_balance
# ---------- CREATE ---------- #

@app.route("/show/new")
def show_new():
    return render_template("show_new.html")


@app.route("/show/create", methods=["POST"])
def show_create():
    #validate
    print(request.form)
    if not model_user_balance.Show.validate_show(request.form):
        return redirect("/show/new")
    # create show
    data = {
        **request.form,
        "user_id": session["uuid"]
    }
    model_user_balance.Show.create(data)
    return redirect("/")

@app.route("/show/<int:id>/edit")
def show_edit(id):
    context = {
        "show": model_user_balance.Show.get_one({"id":id})
    }
    return render_template("show_edit.html", **context)

@app.route("/show/<int:id>/update", methods=["POST"])
def show_update(id):
    #validate
    if not model_user_balance.Show.validate_show(request.form):
        return redirect(f"/show/{id}/edit")

    data = {
        **request.form,
        "id": id
    }

    model_user_balance.Show.update_one(data)
    return redirect("/shows")
    # return redirect(f"/show/{id}/edit")

@app.route("/show/<int:id>/delete")
def show_delete(id):
    model_user_balance.Show.delete_one({"id": id})
    return redirect("/")

@app.route("/show/<int:id>/view")
def show_view(id):
    user_id = model_user_balance.Show.get_one({"id":id}).user_id
    poster_name = model_user.User.get_one({"id":user_id})
    print(poster_name.full_name)
    context = {
        "show": model_user_balance.Show.get_one({"id":id}),
        "name_of_poster": poster_name.full_name
    }
    return render_template("show_view.html", **context)
