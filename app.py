from flask import (Flask, url_for, render_template)

import models

app = Flask(__name__)

@app.route("/")
def index():
    journal = models.Entry.select().limit(5)
    return render_template(url_for('index.html'))

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

if __name__ == '__main__':
    models.initialize()
    journal= models.Entry
    if journal.select().where(journal.id == 1).exists():
        pass
    else:
        models.Entry.create(
            content="Welcome to the Learning Journal!"
        )
    app.run(debug=True, host='127.0.0.1', port=80)