from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FileField, SubmitField, DateField, SelectField, BooleanField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class MessageForm(FlaskForm):
    title = StringField('title', validators=[DataRequired(message='Please input the title')])
    content = StringField('content', validators=[DataRequired(message='Please input the content')])
    submit = SubmitField('Submit')
