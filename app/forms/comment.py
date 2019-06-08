from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FileField, SubmitField, DateField, SelectField, BooleanField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class CommentForm(FlaskForm):
    comment = StringField('comment', validators=[DataRequired(message='Please input the comment')])
    submit = SubmitField('Submit')
