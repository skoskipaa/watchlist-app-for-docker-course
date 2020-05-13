from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user

from application import app, db, bcrypt
from application.auth.models import User
from application.auth.forms import LoginForm
from application.auth.forms import RegisterForm
from sqlalchemy.exc import IntegrityError

@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form = LoginForm())

    form = LoginForm(request.form)

    if not form.validate():
        flash("No such username or password", category="danger")
        return render_template("auth/loginform.html", form = LoginForm())

    user_found = User.query.filter_by(username=form.username.data).first()

    if user_found:
        auth_user = bcrypt.check_password_hash(user_found.password, form.password.data)
        if not auth_user:
            flash("No such username or password", category="danger")
            return render_template("auth/loginform.html", form = form)
    
        login_user(user_found)
        return redirect(url_for("index"))

    flash("No such username or password", category="danger")
    return render_template("auth/loginform.html", form = form)


@app.route("/auth/logout")
def auth_logout():
    logout_user()
    flash("You have been logged out", category="success")
    return redirect(url_for("index"))
    

@app.route("/auth/registration", methods = ["GET"])
def auth_getform():
    return render_template("auth/registrationform.html", form = RegisterForm())


@app.route("/auth/registration", methods = ["POST"])
def auth_register():
    form = RegisterForm(request.form)
    if not form.validate():
        return render_template("auth/registrationform.html", form = form)

    try:
        name = form.name.data
        username = form.username.data
        password = form.password.data

        u = User(name, username, password)

        db.session().add(u)
        db.session().commit()

        flash("New user account created. Please, log in!", category="success")
        return redirect(url_for("auth_login"))

    except IntegrityError:
        flash("Username already taken!", category="danger")
        return render_template("auth/registrationform.html", form = form)
