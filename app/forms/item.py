from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FileField, SubmitField, DateField, SelectField, BooleanField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf.file import FileField, FileAllowed, FileRequired
from app.extensions import photos
from app.models import Item

class UploadForm(FlaskForm):
    item_name = StringField('Item name', validators=[DataRequired(message='Please input the item name')])
    choice_status = [('lost', 'lost'), ('found', 'found'), ('success', 'success')]
    status = SelectField('Lost or Found', choices=choice_status, validators=[DataRequired(message='Please input the location')])
    location = StringField('find/lost Location', validators=[DataRequired(message='Please input the location')])
    time = DateField('Date Order Paid', format='%Y-%m-%d', validators=[DataRequired(message='Please input the time')])
    description = StringField('The description of this item', validators=[DataRequired(message='Please input the description')])
    category = StringField('Category', validators=[DataRequired(message='Please set your category')])
    pic = FileField('Picture', validators=[FileAllowed(photos, message='only can send picture')])
    storage = [('No selection','No selection'), ('T29 Storage', 'T29 Storage'), ('T4 Storage', 'T4 Storage'),
               ('T5 Storage', 'T5 Storage'), ('T6 Storage', 'T6 Storage'), ('T7 Storage', 'T7 Storage'), ('T8 Storage', 'T8 Storage')]
    store_location = SelectField('Store location', choices=storage)
    submit = SubmitField('Submit')

class SearchForm(FlaskForm):
    search = StringField('search', validators=[DataRequired(message='Please input search string')])
    submit = SubmitField('Submit')

