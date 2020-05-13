from application import app, db
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from application.content.models import Content
from application.content.forms import ContentForm

from application.lists.models import Watchlist 

from application.genres.models import Genre

@app.route("/content/<list_id>/new/")
@login_required
def content_form(list_id):
    li = Watchlist.query.filter_by(id=list_id).first()
    return render_template("content/new.html", form = ContentForm(), list_id=li.id)


@app.route("/content/<list_id>", methods=["GET"])
@login_required
def content_for_list(list_id):
    wl = Watchlist.query.get_or_404(list_id)
    acc = wl.account_id

    if not acc == current_user.id:
        flash("Access denied. Please, select a watchlist.", category="warning")
        return redirect(url_for("lists_index"))

    list_name = wl.name
    contentlist = Content.query.filter_by(watchlist_id = list_id).all()
    return render_template("content/list.html", contentlist = contentlist, name=list_name, list_id = list_id,
        watchlist_length = Content.total_length_of_a_watchlist(list_id)) 


@app.route("/content/<list_id>", methods=["POST"])
@login_required
def content_create(list_id):

    wl = Watchlist.query.get_or_404(list_id)
    acc = wl.account_id

    if not acc == current_user.id:
        flash("Access denied.", category="warning")
        return redirect(url_for("lists_index"))

    form = ContentForm(request.form)

    if not form.validate():
        flash("There were some errors. Please, check your input...", category="warning")
        return render_template("content/new.html", form = form, list_id=list_id)

    name = form.name.data
    length = form.length.data
    genres = form.category.data
    cdn = form.cdn.data

    c = Content(name, length, cdn)
    c.watchlist_id = list_id

    for g in genres:
        c.category.append(g)
   
    db.session().add(c)
    db.session().commit()

    return redirect(url_for("content_for_list", list_id = list_id))


@app.route("/content/delete/<content_id>", methods=["POST"])
@login_required
def content_delete(content_id):

    c = Content.query.get(content_id)
    l_id = c.watchlist_id
    db.session().delete(c)
    db.session().commit()

    return redirect(url_for("content_for_list", list_id = l_id))    

@app.route("/content/<content_id>/edit", methods=["GET", "POST"])
@login_required
def content_update(content_id):

    c = Content.query.get_or_404(content_id)
    l_id = c.watchlist_id

    wl = Watchlist.query.get_or_404(l_id)
    acc = wl.account_id

    if not acc == current_user.id:
        flash("Access denied. Please, select a watchlist.", category="warning")
        return redirect(url_for("lists_index"))

    if request.method == "GET":
        form = ContentForm()
        form.name.data = c.name
        form.length.data = c.length
        form.cdn.data = c.cdn
        form.category.data = c.category
       
        return render_template("content/edit.html", form = form, content_id=content_id, name=c.name, list_id=l_id)

    if request.method == "POST":
        form = ContentForm(request.form)

        if not form.validate():
            flash("There were some errors. Please, check your input...", category="warning")
            return render_template("content/edit.html", form = form, content_id=content_id, name = c.name, list_id = l_id)

        c.name = form.name.data
        c.length = form.length.data
        c.category = form.category.data
        c.cdn = form.cdn.data

        db.session().add(c)
        db.session().commit()

        return redirect(url_for("content_for_list", list_id=l_id))

    