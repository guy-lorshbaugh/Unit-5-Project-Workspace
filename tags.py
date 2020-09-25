import datetime
from peewee import *

# import logging
# logger = logging.getLogger('peewee')
# logger.addHandler(logging.StreamHandler())
# logger.setLevel(logging.DEBUG)

db = SqliteDatabase('test.db')

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    username = TextField()

class Tweet(BaseModel):
    content = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)
    user = ForeignKeyField(User, backref='tweets')

class Favorite(BaseModel):
    user = ForeignKeyField(User, backref='favorites')
    tweet = ForeignKeyField(Tweet, backref='favorites')


def populate_test_data():
    db.create_tables([User, Tweet, Favorite])

    data = (
        ('huey', ('meow', 'hiss', 'purr')),
        ('mickey', ('woof', 'whine')),
        ('zaizee', ()))
    for username, tweets in data:
        user = User.create(username=username)
        for tweet in tweets:
            Tweet.create(user=user, content=tweet)

    # Populate a few favorites for our users, such that:
    favorite_data = (
        ('huey', ['whine']),
        ('mickey', ['purr']),
        ('zaizee', ['meow', 'purr']))
    for username, favorites in favorite_data:
        user = User.get(User.username == username)
        for content in favorites:
            tweet = Tweet.get(Tweet.content == content)
            Favorite.create(user=user, tweet=tweet)


def initialize():
    db.connect()
    db.create_tables([BaseModel, User, Tweet, Favorite], safe=True)
    db.close()

initialize()
# populate_test_data()

query = Tweet.select().join(User).where(User.username == 'huey')

for tweet in query:
    print(tweet.content)