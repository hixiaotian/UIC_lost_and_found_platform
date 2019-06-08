from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, FileField, SubmitField, DateField, SelectField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf.file import FileField, FileAllowed, FileRequired

class BroadcastForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(message='Please input the title')])
    content = TextAreaField('Content', validators=[DataRequired(message='Please input the content')])
    submit = SubmitField('Submit')