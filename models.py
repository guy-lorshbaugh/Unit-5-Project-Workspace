import datetime

# from flask_bcrypt import generate_password_hash
# from flask_login import UserMixin
from peewee import *

DATABASE = SqliteDatabase('journal.db')

class Entry(Model):
    date = DateTimeField(default=datetime.datetime.now)
    content = TextField()

    class Meta:
        database = DATABASE
        order_by = ('-date',)

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Entry], safe=True)
    DATABASE.close()

