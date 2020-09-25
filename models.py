import datetime

from peewee import *

DATABASE = SqliteDatabase('journal.db')

class BaseModel(Model):
    class Meta:
        database = DATABASE


class Entry(BaseModel):
    # id = AutoField(unique=True)
    title = CharField(max_length=100)
    date = DateTimeField(default=datetime.datetime.now)
    time_spent = IntegerField(default=0)
    learned = TextField(null=False)
    remember = TextField(default=" ")


class Tags(BaseModel):
    tag = CharField(null=False)


class EntryTags(BaseModel):
    entry_id = ForeignKeyField(Entry)
    tags = ForeignKeyField(Tags)


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Entry, Tags, EntryTags], safe=True)
    DATABASE.close()

# info = Entry.select().where(Entry.id==1).get()
# print(info.learned, info.remember, info.tags)
