import datetime

from flask import (Flask, url_for, render_template, redirect,
                g, flash)
from flask_wtf.csrf import CSRFProtect

import models
import forms

import logging
logger = logging.getLogger('peewee')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

app = Flask(__name__)
app.secret_key ="430po9tgjlkifdsc.p0ow40-23365fg4h,."
csrf = CSRFProtect()
csrf.init_app(app)

@app.route("/")
@app.route("/entries")
def index():
    journal = models.Entry.select().order_by(models.Entry.date.desc())
    return render_template('index.html', journal=journal)


@app.route("/entries/new", methods=('GET', 'POST'))
def create():
    form = forms.Post()
    if form.validate_on_submit():
        models.Entry.create(
            title=form.title.data,
            date=datetime.datetime.combine(form.date.data,
                datetime.datetime.now().time()),
            time_spent=form.time_spent.data,
            learned=form.learned.data,
            remember=form.remember.data
        )
        # tags = form.tags.data.split(',')
        entry = models.Entry.get(models.Entry.title==form.title.data)
        models.EntryTags.create(
            entry_id=entry.id,
            tags=form.tags.data,
        )
        for item in form.tags.data.split(', '):
            models.Tags.create(tag=item)
        flash("Your Entry has been created!")
        return redirect(url_for('index'))
    return render_template('new.html', form=form)


@app.route("/entries/<id>")
def detail(id):
    info = models.Entry.get(models.Entry.id==id)
    # tags = models.EntryTags.get(models.EntryTags.entry_id==id)
    tags = (models.Tags
              .select()
              .join(models.EntryTags)
              .where(models.EntryTags.entry_id==info.id)
              .order_by(models.Tags.tag))
    return render_template("detail.html", id=info, tags=tags)


@app.route("/entries/<id>/edit", methods=('GET', 'POST'))
def edit(id):
    entry = models.Entry.select().where(models.Entry.id==id).get()
    try:
        entry_tags = models.EntryTags.get(models.EntryTags.entry_id==id)
    except:
        entry_tags = None
    form = forms.Post()
    date = datetime.datetime.now()
    if form.validate_on_submit():
        entry.title = form.title.data
        entry.date = date
        entry.time_spent = form.time_spent.data
        entry.learned = form.learned.data
        entry.remember = form.remember.data
        
        for item in form.tags.data.split(', '):
            models.Tags.create(tag=item)
        entry.save()
        if entry_tags != None:
            entry_tags.tags = form.tags.data
            entry_tags.save()
        else:
            models.EntryTags.create(
                entry_id = id,
                tags=form.tags.data
            )
        flash("Your Entry has been edited!")
        return redirect(url_for('index'))
    return render_template("edit.html", form=form, id=id, models=models)


@app.route("/entries/<id>/delete")
def delete(id):
    models.Entry.get(models.Entry.id==id).delete_instance()
    flash("Your journal entry has been deleted.", "deleted")
    return redirect(url_for('index'))


if __name__ == '__main__':
    models.initialize()
    journal= models.Entry
    if journal.select().where(journal.id==1).exists():
        pass
    else:
        models.Entry.create(
            title="Welcome!",
            learned="Welcome to the Learning Journal!",
        )
        models.Tags.create(
            tag="welcome"
        )
    app.run(debug=True, host='127.0.0.1', port=80)

    # info = models.Entry.get(models.Entry.id==2)
    # print(info.id)
    # tags = (models.Tags
    #         .select()
    #         .join(models.EntryTags)
    #         .where(models.EntryTags.entry_id==info.id)
    #         .get())
    # for item in tags:
    #     print(item)

