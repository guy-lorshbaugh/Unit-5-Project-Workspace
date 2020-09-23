import datetime

from peewee import *

DATABASE = SqliteDatabase('journal.db')

class Entry(Model):
    # id = AutoField(unique=True)
    title = CharField(max_length=100)
    date = DateTimeField(default=datetime.datetime.now)
    time_spent = IntegerField(default=0)
    learned = TextField(null=False)
    remember = TextField(default=" ")

    class Meta:
        database = DATABASE


class Tags(Model):
    tag = CharField(null=False)

    class Meta:
        database = DATABASE


class EntryTags(Model):
    entry = ForeignKeyField(Entry)
    tags = ForeignKeyField(Tags, related_name="tag")
    
    class Meta:
        database = DATABASE


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Entry, Tags, EntryTags], safe=True)
    DATABASE.close()

