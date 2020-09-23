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
    tags = CharField(null=False)

    class Meta:
        database = DATABASE


class EntryTags(Model):
    entry = ForeignKeyField(Entry)
    tags = ForeignKeyField(Tags)
    
    class Meta:
        database = DATABASE


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Entry, Tags, EntryTags], safe=True)
    DATABASE.close()

# for item in Tags.select():
#     print(item.id, item.tags)

id_2 = Tags.get(Tags.id==2)

for tag in Tags.select():
    print(tag.tags)

