from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf.file import FileField, FileAllowed, FileRequired
from app.models import User
from app.extensions import photos

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message='Please input your username')])
    student_id = StringField('Student id', validators=[DataRequired(message='Please input your student id')])
    true_name = StringField('True name', validators=[DataRequired(message='Please input the true name')])
    phone_number = StringField('Phone number', validators=[DataRequired(message='Please input your phone number')])
    email = StringField('Email', validators=[DataRequired(message='Please input your email')])
    password = PasswordField('Password', validators=[DataRequired(message='Please input your password'),
                                                     EqualTo('confirm_new_password', message='The confirm is not correct')])
    confirm_new_password = PasswordField('Confirm Password')
    submit = SubmitField('Register')

    def validate_username(self, field):
        user = User.query.filter_by(username=field.data).first()
        if user:
            raise ValidationError('The username already exists')

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if user:
            raise ValidationError('The email already exists')

class LoginForm(FlaskForm):
    username = StringField('username or email', validators=[DataRequired(message='Please input your username')])
    password = PasswordField('keyword', validators=[DataRequired(message='Please input your password')])
    # remember = BooleanField('记住我',default=True)
    submit = SubmitField('login')


class IconForm(FlaskForm):
    icon = FileField('icon', validators=[FileAllowed(photos, message='Only allow picture'), FileRequired(message='Please choose your icon')])
    submit = SubmitField('Upload')

class ModifyProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message='Please input your username')])
    student_id = StringField('Student id', validators=[DataRequired(message='Please input your student id')])
    true_name = StringField('True name', validators=[DataRequired(message='Please input the true name')])
    phone_number = StringField('Phone number', validators=[DataRequired(message='Please input your phone number')])
    email = StringField('Email', validators=[DataRequired(message='Please input your email')])
    submit = SubmitField('Modify')


class ResetPwdForm(FlaskForm):
    old_password = PasswordField('Old password', validators=[DataRequired(message='Please input your old password')])
    new_password = PasswordField('New password', validators=[DataRequired(message='Please input your new password'),
                                                             EqualTo('confirm_new_password', message='The confirm is not correct')])
    confirm_new_password = PasswordField('Confirm new password', validators=[DataRequired(message='Please input your new password')])
    submit = SubmitField('Confirm')


class ChangeStatusForm(FlaskForm):
    change_status = [('administrator', 'administrator'), ('student', 'student'), ('teacher', 'teacher'), ('professor', 'professor'), ('staff', 'staff')]
    choice = SelectField('change status', choices=change_status,
                         validators=[DataRequired(message='Please select the choice')])
    submit = SubmitField('Confirm')

class ChangeStorageForm(FlaskForm):
    storage = [('No selection', 'No selection'), ('T29 Storage', 'T29 Storage'), ('T4 Storage', 'T4 Storage'),
               ('T5 Storage', 'T5 Storage'), ('T6 Storage', 'T6 Storage'), ('T7 Storage', 'T7 Storage'),
               ('T8 Storage', 'T8 Storage')]
    choice = SelectField('Store location', choices=storage, validators=[DataRequired(message='Please input the location')])
    submit = SubmitField('Confirm')