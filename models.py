import datetime

from peewee import *

DATABASE = SqliteDatabase('journal.db')

class BaseModel(Model):
    class Meta:
        database = DATABASE


class Entry(BaseModel):
    title = CharField(max_length=100)
    date = DateTimeField(default=datetime.datetime.now)
    time_spent = IntegerField(default=0)
    learned = TextField(null=False)
    remember = TextField(default=" ")


class Tags(BaseModel):
    tag = CharField(unique=True)


class EntryTags(BaseModel):
    entry_id = ForeignKeyField(Entry)
    tag_id = ForeignKeyField(Tags)


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Entry, Tags, EntryTags], safe=True)
    DATABASE.close()
