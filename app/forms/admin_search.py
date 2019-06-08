from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FileField, SubmitField, DateField, SelectField, BooleanField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class AdminSearchPersonForm(FlaskForm):
    true_name = StringField('true name')
    student_id = StringField('student id')
    upload_item = StringField('upload item')
    submit = SubmitField('Submit')


class AdminSearchItemForm(FlaskForm):
    item_name = StringField('item name')
    uploader = StringField('uploader')
    location = StringField("location")
    submit = SubmitField('Submit')


class AdminSearchChangeLogForm(FlaskForm):
    true_name = StringField('true name')
    item_name = StringField('item name')
    choice = [('No selection', 'No selection'), ('upload', 'upload'), ('modify', 'modify'), ('delete', 'delete')]
    method = SelectField('Method', choices=choice,validators=[DataRequired(message='Please input the choice')])
    submit = SubmitField('Submit')
