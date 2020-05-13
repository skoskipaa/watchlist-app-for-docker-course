from application import app, db
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from application.genres.models import Genre
from application.genres.forms import GenreForm
from sqlalchemy.exc import IntegrityError


@app.route("/genres")
@login_required
def genres_index():
    genrelist = Genre.query.all()
    return render_template("genres/list.html", genrelist = genrelist)

@app.route("/genres/new")
@login_required
def genres_form():
    return render_template("genres/new.html", form = GenreForm())


@app.route("/genres", methods=["POST"])
@login_required
def genres_create():
    form = GenreForm(request.form)

    if not form.validate():
        flash("Please, check your input...", category="warning")
        return render_template("genres/new.html", form = form)

    try:
        name = form.name.data
        g = Genre(name)

        db.session().add(g)
        db.session().commit()

        flash("New genre created!", category="success")
        return redirect(url_for("genres_index"))

    except IntegrityError:
        db.session().rollback()

        flash("Genre already exists!", category="danger")
        return render_template("genres/new.html", form = form)
