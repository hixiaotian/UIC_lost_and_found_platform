from flask import Blueprint, flash, render_template, redirect, url_for, current_app, request, jsonify, Flask
from sqlalchemy import or_
import os
from app.extensions import db
from app.forms import RegisterForm, LoginForm, IconForm, ModifyProfileForm, ResetPwdForm, ChangeStatusForm, AdminSearchItemForm, ChangeStorageForm
from flask_login import login_user, logout_user, current_user, login_required
from app.models import User, Item, Group, Storage
from .item import random_string
from app.extensions import photos
from datetime import datetime

user = Blueprint('user', __name__)


@user.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        user = User.query.filter(User.username == username).first()
        if not user:
            flash('Wrong username or password!')
        elif not user.verify_password(form.password.data):
            flash('Wrong username or password!')
        else:
            login_user(user)
            user.last_login = datetime.now()
            if current_user.group_id == 1:
                return redirect(url_for('main.adminpage'))
            else:
                return redirect(url_for('main.userpage'))
            return redirect('/userpage')
    return render_template('login.html', form=form)

@user.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, student_id=form.student_id.data, true_name=form.true_name.data,
                    phone_number=form.phone_number.data, email=form.email.data, password=form.password.data
                   )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('user.login'))
    return render_template('register.html', form=form)


@user.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('user.login'))

@user.route('/lost_item')
@user.route('/lost_item/<int:page>')
@login_required
def lost_item(page = 1):
    page = request.args.get('page', 1, type=int)
    pagination = Item.query.filter_by(uploader_id=current_user.id, status='lost').order_by(Item.timestamp.desc()).paginate(page, per_page=8, error_out=False)
    posts = pagination.items
    return render_template('personal_lost_item.html', items=posts, pagination=pagination, current_user=current_user)

@user.route('/found_item')
@user.route('/found_item/<int:page>')
@login_required
def found_item(page = 1):
    page = request.args.get('page', 1, type=int)
    pagination = Item.query.filter_by(uploader_id=current_user.id, status='found').order_by(Item.timestamp.desc()).paginate(page, per_page=8, error_out=False)
    posts = pagination.items
    return render_template('personal_found_item.html', items=posts, pagination=pagination, current_user=current_user)


@user.route('/success_item')
@user.route('/success_item/<int:page>')
@login_required
def success_item(page = 1):
    page = request.args.get('page', 1, type=int)
    pagination = Item.query.filter_by(uploader_id=current_user.id, status='success').order_by(Item.timestamp.desc()).paginate(page, per_page=8, error_out=False)
    posts = pagination.items
    return render_template('personal_success_item.html', items=posts, pagination=pagination, current_user=current_user)


@user.route('/total_lost_item', methods=['GET', 'POST'])
@login_required
def total_lost_item():
    if current_user.group_id == 1:
        search_item_name = request.values.get('item_name', type=str, default='')
        search_uploader = request.values.get('uploader_id', type=str, default='')
        search_location = request.values.get('location', type=str, default='')
        page = request.args.get('page', 1, type=int)
        pagination = Item.query.join(User, Item.uploader_id == User.id). \
            filter(Item.item_name.like('%' + search_item_name + '%')). \
            filter(User.username.like('%' + search_uploader + '%')). \
            filter(Item.location.like('%' + search_location + '%')). \
            filter(Item.status == 'lost'). \
            order_by(Item.timestamp.desc()).paginate(page, per_page=8, error_out=False)
        items = pagination.items
        return render_template('admin_lost_item_table.html', items=items, current_user=current_user,
                               pagination=pagination, message='lost ')
    else:
        flash("You are not an administrator!")
        return redirect(url_for('user.login'))

@user.route('/total_found_item', methods=['GET', 'POST'])
@login_required
def total_found_item():
    if current_user.group_id == 1:
        search_item_name = request.values.get('item_name', type=str, default='')
        search_uploader = request.values.get('uploader_id', type=str, default='')
        search_location = request.values.get('location', type=str, default='')
        page = request.args.get('page', 1, type=int)
        pagination = Item.query.join(User, Item.uploader_id == User.id). \
            filter(Item.item_name.like('%' + search_item_name + '%')). \
            filter(User.username.like('%' + search_uploader + '%')). \
            filter(Item.location.like('%' + search_location + '%')). \
            filter(Item.status == 'found'). \
            order_by(Item.timestamp.desc()).paginate(page, per_page=8, error_out=False)
        items = pagination.items
        return render_template('admin_found_item_table.html', items=items, current_user=current_user,
                               pagination=pagination, message='found ')
    else:
        flash("You are not an administrator!")
        return redirect(url_for('user.login'))


@user.route('/total_success_item', methods=['GET', 'POST'])
@login_required
def total_success_item():
    form = AdminSearchItemForm()
    if current_user.group_id == 1:
        search_item_name = request.values.get('item_name', type=str, default='')
        search_uploader = request.values.get('uploader_id', type=str, default='')
        search_location = request.values.get('location', type=str, default='')
        page = request.args.get('page', 1, type=int)
        pagination = Item.query.join(User, Item.uploader_id == User.id). \
            filter(Item.item_name.like('%' + search_item_name + '%')). \
            filter(User.username.like('%' + search_uploader + '%')). \
            filter(Item.location.like('%' + search_location + '%')). \
            filter(Item.status == 'success'). \
            order_by(Item.timestamp.desc()).paginate(page, per_page=8, error_out=False)
        items = pagination.items
        return render_template('admin_success_item_table.html', items=items, current_user=current_user,
                               pagination=pagination, message='success return ')
    else:
        flash("You are not an administrator!")
        return redirect(url_for('user.login'))


@user.route('/modify_icon', methods=['GET'])
@login_required
def modify_icon():
    form = IconForm()
    return render_template('modify_icon.html', form=form, current_user=current_user)


@user.route('/modify_icon_form', methods=['POST'])
@login_required
def modify_icon_form():
    form = IconForm()
    user = User.query.filter_by(id=current_user.id).first()
    if form.validate_on_submit():
        suffix = os.path.splitext(form.icon.data.filename)[1]
        filename = random_string() + suffix
        photos.save(form.icon.data, name=filename)
        user.icon = 'uploads/' + filename
        db.session.commit()
        return 'success'
    return render_template('upload_form.html', form=form, current_user=current_user)


@user.route('/modify_profile', methods=['GET', 'POST'])
@login_required
def modify_profile():
    form = ModifyProfileForm()
    user = User.query.filter_by(id=current_user.id).first()
    if form.validate_on_submit():
        temp = User.query.filter_by(username=form.username.data).first()
        if not temp:
            user.username = form.username.data
            user.true_name = form.true_name.data
            user.student_id = form.student_id.data
            user.email = form.email.data
            user.phone_number = form.phone_number.data
            db.session.commit()
            return redirect(url_for('main.userpage'))
        elif current_user.username == temp.username:
            user.true_name = form.true_name.data
            user.student_id = form.student_id.data
            user.email = form.email.data
            user.phone_number = form.phone_number.data
            db.session.commit()
            return redirect(url_for('main.userpage'))
        else:
            flash("This is an existed username")
            render_template('modify_basic_person.html', form=form, current_user=current_user)
    return render_template('modify_basic_person.html', form=form, current_user=current_user)


@user.route('/admin_modify_profile/<int:user_id>', methods=['GET', 'POST'])
@login_required
def admin_modify_profile(user_id):
    form = ModifyProfileForm()
    user = User.query.filter_by(id=user_id).first()
    if current_user.group_id == 1:
        if form.validate_on_submit():
            temp = User.query.filter_by(username=form.username.data).first()
            if not temp:
                user.username = form.username.data
                user.true_name = form.true_name.data
                user.student_id = form.student_id.data
                user.email = form.email.data
                user.phone_number = form.phone_number.data
                db.session.commit()
                return render_template('admin_person_table.html', form=form, current_user=user)
            elif user.username == temp.username:
                user.true_name = form.true_name.data
                user.student_id = form.student_id.data
                user.email = form.email.data
                user.phone_number = form.phone_number.data
                db.session.commit()
                return render_template('admin_person_table.html', form=form, current_user=user)
            else:
                flash("This is an existed username")
                render_template('modify_basic_person.html', form=form, current_user=current_user)
        return render_template('modify_basic_person.html', form=form, current_user=current_user)
    flash('You are not an administrator')
    redirect(url_for('user.login'))


@user.route('/modify_password', methods=['GET', 'POST'])
@login_required
def modify_password():
    form = ResetPwdForm()
    user = User.query.filter_by(id=current_user.id).first()
    if form.validate_on_submit():
        oldpwd = form.old_password.data
        if user.verify_password(oldpwd):
            newpwd = form.new_password.data
            user.password = newpwd
            logout_user()
            return redirect(url_for('user.login'))
        else:
            flash('The old password is not correct')
    return render_template('modify_password.html', form=form, current_user=current_user)


@user.route('/modify_status/<user_id>', methods=['GET', 'POST'])
@login_required
def modify_status(user_id):
    form = ChangeStatusForm()
    if current_user.group_id == 1:
        user = User.query.filter_by(id=user_id).first()
        if form.validate_on_submit():
            group = Group.query.filter_by(group_name=form.choice.data).first()
            user.group_id = group.id
            db.session.commit()
            return redirect(url_for('main.adminpage'))
        return render_template('modify_person_status.html', form=form, current_user=current_user, user=user)
    flash('You are not an administrator')
    redirect(url_for('user.login'))


@user.route('/change_storage', methods=['GET', 'POST'])
@login_required
def changeStorage():
    form = ChangeStorageForm()
    if current_user.group_id == 1:
        if form.validate_on_submit():
            storage = Storage.query.filter_by(location_name=form.choice.data).first()
            current_user.storage_id = storage.id
            return redirect(url_for('main.showStorage', storage_id=storage.id))
        return render_template('change_storage.html', form=form, current_user=current_user)
    flash('You are not an administrator')
    redirect(url_for('user.login'))