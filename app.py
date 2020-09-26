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


def get_tags(id):
    """Selects entry tags by Entry PrimaryKey."""
    tags = (models.Tags
        .select()
        .join(models.EntryTags)
        .join(models.Entry)
        .where(models.Entry.id == id)
        .order_by(models.Tags.id)
        )
    return tags
    

def del_tags(id):
    """Deletes tag associations in EntryTags by entry_id."""
    query = (models.EntryTags
                .select()
                .where(models.EntryTags.entry_id == id)
            )
    for item in query:
        item.delete_instance()


@app.route("/")
@app.route("/entries")
def index():
    journal = models.Entry.select().order_by(models.Entry.date.desc())
    return render_template('index.html', journal=journal, models=models)


@app.route("/entries/<id>")
def detail(id):
    info = models.Entry.get(models.Entry.id==id)
    return render_template("detail.html", id=info, tags=get_tags(id))


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
        tags_list = form.tags.data.split(', ')
        entry = models.Entry.get(models.Entry.title == form.title.data)
        for item in tags_list:
            try:
                models.Tags.create(tag=item)
            except:
                pass
        for tag in tags_list:
            tag_data = models.Tags.get(models.Tags.tag == tag)
            models.EntryTags.create(
                entry_id=entry.id,
                tag_id=tag_data
            )
        flash("Your Entry has been created!")
        return redirect(url_for('index'))
    return render_template('new.html', form=form)


@app.route("/entries/<id>/edit", methods=('GET', 'POST'))
def edit(id):
    entry = models.Entry.select().where(models.Entry.id == id).get()
    tags_list = []
    for tag in get_tags(id):
        tags_list.append(tag.tag)
    tags = ", ".join(tags_list)
    form = forms.Post()
    if form.validate_on_submit():
        entry.title = form.title.data
        entry.date = (datetime.datetime
                        .combine(form.date.data, entry.date.time())
                        )
        entry.time_spent = form.time_spent.data
        entry.learned = form.learned.data
        entry.remember = form.remember.data
        for item in form.tags.data.split(', '):
            try:
                models.Tags.create(tag=item)
            except:
                pass
        entry.save()
        del_tags(id)
        for tag in form.tags.data.split(', '):
            tag_data = models.Tags.get(models.Tags.tag == tag)
            models.EntryTags.create(
                entry_id=entry.id,
                tag_id=tag_data.id
            )
        flash("Your Entry has been edited!")
        return redirect(url_for('index'))
    return render_template("edit.html", form=form, id=id, 
                            models=models, tags=tags)

@app.route("/entries/<tag>/tag")
def tag(tag):
    query = (models.Entry
                .select()
                .join(models.EntryTags)
                .join(models.Tags)
                .where(models.Tags.tag == tag)
    )
    return render_template("tag.html", models=models, id=query)



@app.route("/entries/<id>/delete")
def delete(id):
    models.Entry.get(models.Entry.id==id).delete_instance()
    del_tags(id)
    flash("Your journal entry has been deleted.")
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
    app.run(debug=True, host='127.0.0.1', port=80)
