from flask import Blueprint, flash, render_template, redirect, url_for, current_app, request, jsonify
from sqlalchemy import or_
from app.extensions import db, photos
from app.forms import RegisterForm, LoginForm
from flask_login import login_user, logout_user, current_user, login_required
from app.models import Item, User, Group, Broadcast, Comment, Storage, Message, Change, Category
from app.forms import BroadcastForm, MessageForm, AdminSearchPersonForm, AdminSearchChangeLogForm, AdminSearchItemForm, ModifyStorageForm, ChangeStorageForm
from .item import random_string
import os

main = Blueprint('main', __name__)
import datetime


@main.route('/')
def index():
    if Group.query.count() == 0:
        admin = Group(group_name='administrator')
        db.session.add(admin)
        student = Group(group_name='student')
        db.session.add(student)
        teacher = Group(group_name='teacher')
        db.session.add(teacher)
        professor = Group(group_name='professor')
        db.session.add(professor)
        staff = Group(group_name='staff')
        db.session.add(staff)
    if Storage.query.count() == 0:
        T29 = Storage(location_name='T29 Storage', available_time='9a.m.-12p.m.', phone_number=13124242523)
        T4 = Storage(location_name='T4 Storage', available_time='9a.m.-12p.m.', phone_number=13124242523)
        T5 = Storage(location_name='T5 Storage', available_time='9a.m.-12p.m.', phone_number=13124242523)
        T6 = Storage(location_name='T6 Storage', available_time='9a.m.-12p.m.', phone_number=13124242523)
        T7 = Storage(location_name='T7 Storage', available_time='9a.m.-12p.m.', phone_number=13124242523)
        T8 = Storage(location_name='T8 Storage', available_time='9a.m.-12p.m.', phone_number=13124242523)
        db.session.add(T29)
        db.session.add(T4)
        db.session.add(T5)
        db.session.add(T6)
        db.session.add(T7)
        db.session.add(T8)
    if Category.query.count() == 0:
        electronic = Category(name="electronic")
        living_thing = Category(name="living_thing")
        valuables = Category(name="valuables")
        card = Category(name="card")
        school_supplies = Category(name="school_supplies")
        book = Category(name="book")
        others = Category(name="others")
        db.session.add(electronic)
        db.session.add(living_thing)
        db.session.add(valuables)
        db.session.add(card)
        db.session.add(school_supplies)
        db.session.add(book)
        db.session.add(others)
    user_count = User.query.count()
    found_count = Item.query.filter_by(status='found').count()
    lost_count = Item.query.filter_by(status='lost').count()
    success_count = Item.query.filter_by(status='success').count()
    return render_template('index.html', user_count=user_count, found_count=found_count, lost_count=lost_count,
                           success_count=success_count, current_user=current_user)


@main.route('/userpage', methods=['GET', 'POST'])
@login_required
def userpage():
    if current_user.is_authenticated:
        if current_user.group_id != 1:
            found_count = Item.query.filter_by(uploader_id=current_user.id, status='found').count()
            lost_count = Item.query.filter_by(uploader_id=current_user.id, status='lost').count()
            success_count = Item.query.filter_by(uploader_id=current_user.id, status='success').count()
            broadcasts = Broadcast.query.order_by(Broadcast.timestamp.desc()).all()
            comments = Comment.query.filter_by(comment_item=Item.id).join(Item,
                                                                          Item.uploader_id == current_user.id).order_by(
                Comment.timestamp.desc()).all()
            page = request.args.get('page', 1, type=int)
            pagination = Item.query.filter_by(uploader_id=current_user.id).order_by(
                Item.timestamp.desc()).paginate(page, per_page=10, error_out=False)
            items = pagination.items
            messages = Message.query.filter_by(sender_id=current_user.id, is_recieve=True).all()
            return render_template('personal_page.html', current_user=current_user, lost_count=lost_count,
                                   found_count=found_count, success_count=success_count, pagination=pagination,
                                   email=current_user.email, phone_number=current_user.phone_number, items=items,
                                   icon=current_user.icon, broadcasts=broadcasts, comments=comments, messages=messages)
        else:
            return redirect(url_for('main.adminpage'))
    else:
        flash('You should login first!')
        return redirect('user.login')



@main.route('/manage_user', methods=['GET', 'POST'])
def manageUser():
    if current_user.group_id == 1:
        search_true_name = request.values.get('true_name', type=str, default='')
        search_student_id = request.values.get('student_id', type=str, default='')
        search_upload_item = request.values.get('upload_item', type=str, default='')
        page = request.args.get('page', 1, type=int)
        if search_upload_item == '':
            pagination = User.query.filter(User.true_name.like('%' + search_true_name + '%')).filter(User.student_id.like('%' + search_student_id + '%')). \
                order_by(User.last_login.desc()).paginate(page, per_page=8, error_out=False)
        else:
            pagination = User.query.join(Item, Item.uploader_id == User.id).filter(
            Item.item_name.like('%' + search_upload_item + '%')). \
            filter(User.true_name.like('%' + search_true_name + '%')).filter(
            User.student_id.like('%' + search_student_id + '%')). \
            order_by(User.last_login.desc()).paginate(page, per_page=8, error_out=False)
        users = pagination.items
        return render_template('admin_person_table.html', users=users, current_user=current_user,
                               pagination=pagination, message='')
    flash('You are not an administrator!')
    return redirect(url_for('user.login'))


@main.route('/manage_item', methods=['GET', 'POST'])
def manageItem():
    if current_user.group_id == 1:
        search_item_name = request.values.get('item_name', type=str, default='')
        search_uploader = request.values.get('uploader_id', type=str, default='')
        search_location = request.values.get('location', type=str, default='')
        page = request.args.get('page', 1, type=int)
        pagination = Item.query.join(User, Item.uploader_id == User.id). \
            filter(Item.item_name.like('%' + search_item_name + '%')). \
            filter(User.username.like('%' + search_uploader + '%')). \
            filter(Item.location.like('%' + search_location + '%')). \
            order_by(Item.timestamp.desc()).paginate(page, per_page=8, error_out=False)
        items = pagination.items
        return render_template('admin_item_table.html', items=items, current_user=current_user,
                               pagination=pagination)
    flash('You are not an administrator!')
    return redirect(url_for('user.login'))


@main.route('/manage_item_by_uploader/<int:uploader_id>/', methods=['GET', 'POST'])
def manageItemByUploader(uploader_id):
    if current_user.group_id == 1:
        user = User.query.filter_by(id=uploader_id).first()
        search_item_name = request.values.get('item_name', type=str, default='')
        search_uploader = request.values.get('uploader_id', type=str, default='')
        search_location = request.values.get('location', type=str, default='')
        page = request.args.get('page', 1, type=int)
        pagination = Item.query.join(User, Item.uploader_id == User.id). \
            filter(Item.item_name.like('%' + search_item_name + '%')). \
            filter(User.username.like('%' + search_uploader + '%')). \
            filter(Item.location.like('%' + search_location + '%')). \
            filter(Item.uploader_id == uploader_id). \
            order_by(Item.timestamp.desc()).paginate(page, per_page=8, error_out=False)
        items = pagination.items
        return render_template('admin_uploader_item_table.html', items=items, current_user=current_user,
                               pagination=pagination, user=user, message=user.username+' uploaded ')
    flash('You are not an administrator!')
    return redirect(url_for('user.login'))


@main.route('/manage_found_item_by_storage/<int:storage_id>', methods=['GET', 'POST'])
def manageFoundItemByStorage(storage_id):
    if current_user.group_id == 1:
        storage = Storage.query.filter_by(id=storage_id).first()
        search_item_name = request.values.get('item_name', type=str, default='')
        search_uploader = request.values.get('uploader', type=str, default='')
        search_location = request.values.get('location', type=str, default='')
        page = request.args.get('page', 1, type=int)
        pagination = Item.query.filter(Item.store_location_id == storage.id).join(User, Item.uploader_id == User.id). \
            filter(Item.item_name.like('%' + search_item_name + '%')). \
            filter(User.username.like('%' + search_uploader + '%')). \
            filter(Item.location.like('%' + search_location + '%')). \
            filter(Item.status == 'found'). \
            order_by(Item.timestamp.desc()).paginate(page, per_page=8, error_out=False)
        items = pagination.items
        return render_template('storage_found_item_table.html', items=items, current_user=current_user,
                               pagination=pagination, storage=storage, message=storage.location_name + ' found ')
    flash('You are not an administrator!')
    return redirect(url_for('user.login'))


@main.route('/manage_success_item_by_storage/<int:storage_id>', methods=['GET', 'POST'])
def manageSuccessItemByStorage(storage_id):
    if current_user.group_id == 1:
        storage=Storage.query.filter_by(id=storage_id).first()
        search_item_name = request.values.get('item_name', type=str, default='')
        search_uploader = request.values.get('uploader_id', type=str, default='')
        search_location = request.values.get('location', type=str, default='')
        page = request.args.get('page', 1, type=int)
        pagination = Item.query.join(User, Item.uploader_id == User.id). \
            filter(Item.item_name.like('%' + search_item_name + '%')). \
            filter(User.username.like('%' + search_uploader + '%')). \
            filter(Item.location.like('%' + search_location + '%')). \
            filter(storage_id == storage.id). \
            filter(Item.status == 'success'). \
            order_by(Item.timestamp.desc()).paginate(page, per_page=8, error_out=False)
        items = pagination.items
        return render_template('storage_success_item_table.html', items=items, current_user=current_user,
                               pagination=pagination, storage=storage, message=storage.location_name + ' success return ')
    flash('You are not an administrator!')
    return redirect(url_for('user.login'))


@main.route('/adminpage', methods=['GET'])
@login_required
def adminpage():
    if current_user.is_authenticated:
        if current_user.group_id == 1:
            found_count = Item.query.filter_by(status='found').count()
            lost_count = Item.query.filter_by(status='lost').count()
            success_count = Item.query.filter_by(status='success').count()
            broadcasts = Broadcast.query.order_by(Broadcast.timestamp.desc()).all()
            return render_template('admin_page.html', current_user=current_user, lost_count=lost_count,
                                   found_count=found_count, success_count=success_count,
                                   email=current_user.email, phone_number=current_user.phone_number,
                                   icon=current_user.icon, broadcasts=broadcasts)
        else:
            flash('You are not an administrator!')
            return redirect(url_for('user.login'))
    flash('You should login first!')
    return redirect(url_for('user.login'))


@main.route('/create_broadcast', methods=['GET', 'POST'])
@login_required
def createBroadcast():
    if current_user.group_id == 1:
        form = BroadcastForm()
        if form.validate_on_submit():
            broadcast = Broadcast(uploader_id=current_user.id, title=form.title.data, content=form.content.data)
            db.session.add(broadcast)
            db.session.commit()
            return redirect(url_for('main.adminpage'))
        return render_template('create_broadcast.html', current_user=current_user, form=form)
    else:
        flash('You are not an administrator!')
        return redirect(url_for('user.login'))


@main.route('/show_broadcast', methods=['GET'])
@main.route('/show_broadcast/<int:page>', methods=['GET'])
@login_required
def showBroadcast(page=1):
    page = request.args.get('page', 1, type=int)
    pagination = Broadcast.query.order_by(Broadcast.timestamp.desc()).paginate(page, per_page=8, error_out=False)
    broadcasts = pagination.items
    return render_template('view_broadcast.html', broadcasts=broadcasts, current_user=current_user,
                           pagination=pagination)


@main.route('/show_comment', methods=['GET'])
@main.route('/show_comment/<int:page>', methods=['GET'])
@login_required
def showComment(page=1):
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.order_by(Comment.timestamp.desc()).filter_by(comment_item=Item.id).join(Item, Item.uploader_id == current_user.id).paginate(
        page, per_page=8, error_out=False)
    comments = pagination.items
    return render_template('view_comment.html', comments=comments, current_user=current_user, pagination=pagination)


@main.route('/view_storage/<int:storage_id>', methods=['GET', 'POST'])
@main.route('/view_storage/<int:storage_id>/<int:page>', methods=['GET', 'POST'])
@login_required
def showStorage(storage_id, page=1):
    storage = Storage.query.filter_by(id=storage_id).first()
    found_count = Item.query.filter_by(store_location_id=storage.id, status='found').count()
    success_count = Item.query.filter_by(store_location_id=storage.id, status='success').count()
    page = request.args.get('page', 1, type=int)
    pagination = Item.query.filter_by(store_location_id=storage.id).order_by(Item.timestamp.desc()).paginate(page, per_page=10, error_out=False)
    items = pagination.items
    form = MessageForm()
    if current_user.group_id == 1:
        messages = Message.query.filter_by(store_location_id=storage_id, is_recieve=0).order_by(Message.timestamp.desc()).all()
        return render_template('storage_location.html', current_user=current_user, storage=storage,
                               found_count=found_count, success_count=success_count, items=items, form=form,
                               messages=messages, pagination=pagination)
    if form.validate_on_submit():
        message = Message(sender_id=current_user.id, title=form.title.data, content=form.content.data,
                          store_location_id=storage_id)
        db.session.add(message)
        success_send = 'You are succeed sending the message to this storage!'
        return render_template('storage_location.html', current_user=current_user, storage=storage,
                               found_count=found_count, success_count=success_count, items=items,
                               success_send=success_send, form=form, pagination=pagination)
    return render_template('storage_location.html', current_user=current_user, storage=storage,pagination=pagination,
                           found_count=found_count, success_count=success_count, items=items, form=form)

@main.route('/modify_storage/<int:storage_id>', methods=['GET'])
@login_required
def modifyStorage(storage_id):
    form = ModifyStorageForm()
    storage = Storage.query.filter_by(id=storage_id).first()
    return render_template('modify_storage.html', form=form, storage=storage, current_user=current_user)


@main.route('/modify_storage/<int:storage_id>', methods=['POST'])
@login_required
def modifyStorage_form(storage_id):
    form = ModifyStorageForm()
    if current_user.group_id == 1:
        storage = Storage.query.filter_by(id=storage_id).first()
        if form.validate_on_submit():
            suffix = os.path.splitext(form.pic.data.filename)[1]
            filename = random_string() + suffix
            photos.save(form.pic.data, name=filename)
            storage.pic = 'uploads/' + filename
            storage.available_time = form.available_time.data
            storage.phone_number = form.phone_number.data
            return 'success'
        return render_template('upload_form.html', form=form, current_user=current_user)
    else:
        flash('You are not an administrator!')
        return redirect(url_for('user.login'))



@main.route('/view_message/<int:storage_id>', methods=['GET'])
@main.route('/view_message/<int:storage_id>/<int:page>', methods=['GET'])
@login_required
def showMessage(storage_id, page=1):
    if current_user.group_id == 1:
        storage = Storage.query.filter_by(id=storage_id).first()
        page = request.args.get('page', 1, type=int)
        pagination = Message.query.filter_by(store_location_id=storage_id, is_recieve=0).order_by(Message.timestamp.desc()).paginate(
            page, per_page=8, error_out=False)
        messages = pagination.items
        return render_template('view_message.html', storage=storage, messages=messages, current_user=current_user,
                               pagination=pagination)
    else:
        flash('You are not an administrator!')
        return redirect(url_for('user.login'))


@main.route('/user_message/', methods=['GET'])
@main.route('/user_message/<int:page>', methods=['GET'])
@login_required
def userMessage(page=1):
    page = request.args.get('page', 1, type=int)
    pagination = Message.query.filter_by(sender_id=current_user.id, is_recieve=True).order_by(
        Message.timestamp.desc()).paginate(page, per_page=8, error_out=False)
    messages = pagination.items
    return render_template('view_message.html', messages=messages, current_user=current_user, pagination=pagination)


@main.route('/reply/<int:storage_id>/<int:reply_id>', methods=['GET', 'POST'])
@login_required
def reply(storage_id, reply_id):
    if current_user.group_id == 1:
        form = MessageForm()
        storage = Storage.query.filter_by(id=storage_id).first()
        message_view = Message.query.filter_by(sender_id=reply_id).first()
        if form.validate_on_submit():
            message = Message(sender_id=reply_id, title=form.title.data, content=form.content.data,
                              store_location_id=storage.id, is_recieve=True)
            db.session.add(message)
            flash('send success!')
            return redirect(url_for('main.showStorage', storage_id=storage_id))
        return render_template('reply_message.html', storage=storage, message_view=message_view, form=form)
    else:
        flash('You are not an administrator!')
        return redirect(url_for('user.login'))


@main.route('/change_log', methods=['GET', 'POST'])
@login_required
def changeLog():
    search_true_name = request.values.get('true_name', type=str, default='')
    search_item_name = request.values.get('item_name', type=str, default='')
    search_method = request.values.get('method', type=str, default='')
    if search_method == 'No selection':
        search_method = ''
    page = request.args.get('page', 1, type=int)
    pagination = Change.query.join(User, User.id == Change.changer_id). \
        filter(User.true_name.like('%' + search_true_name + '%')). \
        filter(Change.item_name.like('%' + search_item_name + '%')). \
        filter(Change.method.like('%' + search_method + '%')). \
        order_by(Change.timestamp.desc()).paginate(page, per_page=10, error_out=False)
    changes = pagination.items
    return render_template('change_log.html', changes=changes, current_user=current_user, pagination=pagination)

@main.route('/contact_us', methods=['GET'])
@login_required
def contactUs():
    return render_template('contact_us.html', current_user=current_user)

