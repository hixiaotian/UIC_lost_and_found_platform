from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FileField, SubmitField, DateField, SelectField, BooleanField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf.file import FileField, FileAllowed, FileRequired
from app.extensions import photos

class ModifyStorageForm(FlaskForm):
    available_time = StringField('available time', validators=[DataRequired(message='Please input the time')])
    phone_number = StringField('phone number', validators=[DataRequired(message='Please input the phone number')])
    pic = FileField('Picture', validators=[FileAllowed(photos, message='only can send picture'),
                                           FileRequired(message='please select file first')])
    submit = SubmitField('Submit')
