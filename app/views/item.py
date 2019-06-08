from flask import Blueprint, flash, render_template, redirect, url_for, current_app, request, jsonify
from sqlalchemy import or_
import os
from app.extensions import db, photos
from app.forms import UploadForm, SearchForm, CommentForm
from flask_login import login_user, logout_user, current_user, login_required
from app.models import Item, User, Comment, Storage, Change, Category
from app.config import Config
from flask_sqlalchemy import SQLAlchemy

item = Blueprint('item', __name__)

def random_string(length=32):
    import random
    import string
    base_str = string.ascii_letters + string.digits
    return ''.join(random.choice(base_str) for _ in range(length))

@item.route('/upload', methods=['GET'])
@login_required
def upload():
    form = UploadForm()
    return render_template('upload.html', form=form)


@item.route('/upload_form', methods=['POST'])
@login_required
def upload_form():
    form = UploadForm()
    if form.validate_on_submit():
        if not form.pic.data:
            flash('Please select the file')
        else:
            suffix = os.path.splitext(form.pic.data.filename)[1]
            filename = random_string() + suffix
            photos.save(form.pic.data, name=filename)
            category = Category.query.filter_by(name=form.category.data).first()
            if form.store_location.data == 'No selection':
                item = Item(item_name=form.item_name.data, status=form.status.data, location=form.location.data,
                            time=form.time.data, category_id=category.id, description=form.description.data,
                            pic=filename, uploader_id=current_user.id)
            else:
                storage = Storage.query.filter_by(location_name=form.store_location.data).first()
                item = Item(item_name=form.item_name.data, status=form.status.data, location=form.location.data,
                            time=form.time.data, category_id=category.id, description=form.description.data,
                            pic=filename, uploader_id=current_user.id, store_location_id=storage.id)
            db.session.add(item)
            item_change = Item.query.filter_by(item_name=form.item_name.data, time=form.time.data, location=form.location.data, description=form.description.data).first()
            change = Change(changer_id=current_user.id, method='upload', item_id=item_change.id, item_name=item_change.item_name,
            content = 'create a ' + form.status.data + ' item named ' + form.item_name.data)
            db.session.add(change)
            db.session.commit()
            return 'success'
    return render_template('upload_form.html', form=form, current_user=current_user)


@item.route('/search', methods = ['GET', 'POST'])
@login_required
def search():
    searching = request.values.get("search", type=str, default="")
    category_name = request.values.get("category", type=str, default=None)
    category = Category.query.filter_by(name=category_name).first()
    page = request.values.get("page", type=int, default=1)
    print(page)
    if not category:
        pagination = Item.query.filter(Item.item_name.like('%' + searching + '%')).\
            order_by(Item.timestamp.desc()).paginate(page, per_page=8, error_out=False)
    else:
        pagination = Item.query.filter(Item.item_name.like('%' + searching + '%')).\
            filter(Item.category_id == category.id).\
            order_by(Item.timestamp.desc()).paginate(page, per_page=8, error_out=False)
    posts = pagination.items
    return render_template('search.html', items=posts, pagination=pagination, search=searching,
                           current_user=current_user)


@item.route('/detail/<item_id>', methods=['GET', 'POST'])
@item.route('/detail/<item_id>/<int:page>', methods=['GET', 'POST'])
@login_required
def itemDetail(item_id, page=1):
    item = Item.query.filter_by(id=item_id).first()
    uploader = User.query.filter_by(id=item.uploader_id).first()
    form = CommentForm()
    if form.validate_on_submit():
        comment_content = form.comment.data
        comment = Comment(uploader_id=current_user.id, comment_item=item_id, content=comment_content)
        db.session.add(comment)
        db.session.commit()
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.filter_by(comment_item=item_id).order_by(Comment.timestamp.desc()).paginate(page, per_page=6, error_out=False)
    comment_show = pagination.items
    return render_template('item_detail.html', item=item, uploader=uploader, current_user=current_user, pagination=pagination,
                           comment=comment_show, form=form)


@item.route('/modify/<item_id>', methods=['GET', 'POST'])
@login_required
def modify(item_id):
    item = Item.query.filter_by(id=item_id).first()
    form = UploadForm()
    return render_template('modify_item.html', form=form, item=item, current_user=current_user)


@item.route('/modify_form/<item_id>', methods=['POST'])
@login_required
def modify_form(item_id):
    form = UploadForm()
    item = Item.query.filter_by(id=item_id).first()
    if form.validate_on_submit():
        if form.pic.data:
            suffix = os.path.splitext(form.pic.data.filename)[1]
            filename = random_string() + suffix
            photos.save(form.pic.data, name=filename)
            item.pic = filename
        category = Category.query.filter_by(name=form.category.data).first()
        item.item_name = form.item_name.data
        item.status = form.status.data
        item.location = form.location.data
        item.time = form.time.data
        item.category_id = category.id
        item.description = form.description.data
        change = Change(changer_id=current_user.id, method='modify', item_id=item.id, item_name=item.item_name,
                        content='change a ' + form.status.data + ' item named ' + form.item_name.data)
        db.session.add(change)
        if form.store_location.data != 'No selection':
            storage = Storage.query.filter_by(location_name=form.store_location.data).first()
            item.store_location_id = storage.id
        db.session.commit()
        return 'success'
    return render_template('upload_form.html', form=form, current_user=current_user)

@item.route('/delete/<item_id>', methods=['GET'])
@login_required
def delete(item_id):
    item = Item.query.filter_by(id=item_id).first()
    change = Change(changer_id=current_user.id, method='delete', item_id=item.id, item_name=item.item_name,
                    content='delete a ' + item.status + ' item named ' + item.item_name)
    db.session.add(change)
    db.session.delete(item)
    return redirect(url_for('main.userpage'))


@item.route('/change_status/<item_id>', methods=['GET'])
@login_required
def ChangeStatus(item_id):
    item = Item.query.filter_by(id=item_id).first()
    change = Change(changer_id=current_user.id, method='modify', item_id=item.id, item_name=item.item_name,
                    content='successfully return a ' + item.status + ' item named ' + item.item_name)
    db.session.add(change)
    item.status = 'success'

    return redirect(url_for('item.itemDetail',item_id=item_id))