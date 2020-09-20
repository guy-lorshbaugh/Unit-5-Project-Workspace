import datetime

from flask_wtf import Form
from wtforms import (StringField, PasswordField, TextAreaField, 
    DateField, IntegerField)
from wtforms.validators import DataRequired, length

import models

class Post(Form):
    title = StringField(u"Title", validators=[
        DataRequired(),
        length(max=100)
    ])  
    date = DateField(default=datetime.date.today())
    time_spent = IntegerField(u"Time Spent (round to nearest hour)",
        validators=[
                    DataRequired(),
                ])
    learned = TextAreaField(u"What did you learn?", validators=[
                DataRequired(),
            ])
    remember = TextAreaField(u"Links and other things to remember")


class Edit(Form):
    form = models.Entry
    title = StringField(u"Title", validators=[
        DataRequired(),
        length(max=100)
    ])  
    date = DateField(default=datetime.date.today())
    time_spent = IntegerField(u"Time Spent (round to nearest hour)", 
        validators=[
                    DataRequired(),
                ])
    learned = TextAreaField(u"What did you learn?", validators=[
                DataRequired(),
            ])
    remember = TextAreaField(u"Links and other things to remember")
    