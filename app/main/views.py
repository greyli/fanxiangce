# -*-coding: utf-8-*-
import os
from datetime import datetime
from flask import render_template, session, redirect, \
    url_for, flash, abort, request, current_app
from flask_login import login_required, current_user
from werkzeug import secure_filename


from . import main
from .forms import TagForm, WallForm, NormalForm, EditProfileForm, EditProfileAdminForm, TESTForm, CommentForm
from .. import db
from ..models import User, Role, Permission, Album, Photo, Like, Comment
from tag import glue
from wall import wall
from ..decorators import admin_required, permission_required



@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    albums = user.albums.order_by(Album.timestamp.desc()).all()
    album_count = len(albums)
    photo_count = sum([len(album.photos.order_by(Photo.timestamp.asc()).all()) for album in albums])
    return render_template('user.html', user=user, albums=albums, album_count=album_count, photo_count=photo_count)


@main.route('/user/<username>/albums')
def albums(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    albums = user.albums.order_by(Album.timestamp.desc()).all()
    album_count = len(albums)
    return render_template('albums.html', user=user, albums=albums, album_count=album_count)

@main.route('/user/<username>/likes')
def likes(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    likes = user.likes.order_by(Like.timestamp.desc()).all()
    like_count = len(likes)
    likes = [{'user': like.like, 'timestamp': like.timestamp, 'path':like.like.path} for like in likes]
    return render_template('likes.html', user=user, likes=likes, like_count=like_count)

@main.route('/album/<int:id>')
def album(id):
    album = Album.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    pagination = album.photos.order_by(Photo.timestamp.asc()).paginate(
        page, per_page=20, error_out=False
    )
    photos = pagination.items

    for photo in photos:
        liked_count = []
        liked = photo.liked.order_by(Like.timestamp.desc()).all()
        liked_count.append(len(liked))

    if current_user.is_authenticated:
        user = User.query.filter_by(username=current_user.username).first()
        likes = user.likes.order_by(Like.timestamp.desc()).all()
        likes = [{'id': like.like, 'timestamp': like.timestamp, 'path': like.like.path} for like in likes]
        like_list = [like['path'] for like in likes]
    else:
        likes = ""
        like_list = []

    if album.type == 1:
        files = []
        for photo in photos:
            files.append(photo.path)
        html = wall()
        return render_template('wall.html', album=album, html=html)
    return render_template('album.html', album=album, photos=photos, pagination=pagination,
                           like_list=like_list, likes=likes, liked_count=[liked_count])


@main.route('/photo/<int:id>', methods=['GET', 'POST'])
def photo(id):
    photo = Photo.query.get_or_404(id)
    album = photo.album
    form = CommentForm()
    photo_index = [p.id for p in album.photos.order_by(Photo.timestamp.asc())].index(photo.id) + 1
    page = request.args.get('page', photo_index, type=int)
    pagination = album.photos.order_by(Photo.timestamp.asc()).paginate(
        page, per_page=1, error_out=False
    )
    photos = pagination.items

    if current_user.is_authenticated:
        user = User.query.filter_by(username=current_user.username).first()
        likes = user.likes.order_by(Like.timestamp.desc()).all()
        likes = [{'id': like.like, 'timestamp': like.timestamp, 'path': like.like.path} for like in likes]
        like_list = [like['path'] for like in likes]
    else:
        likes = ""
        like_list = []

    if form.validate_on_submit() and current_user.is_authenticated:
        comment = Comment(body=form.body.data,
                          photo=photo,
                          author=current_user._get_current_object())
        db.session.add(comment)
        flash(u'你的评论已经发表。')
        return redirect(url_for('photo', id=photo.id, page=-1))
    comments = photo.comments.order_by(Comment.timestamp.asc()).all()
    return render_template('photo.html', form=form, album=album, photos=photos,
                           like_list=like_list, pagination=pagination, comments=comments, photo_index=photo_index)


@main.route('/edit-profile', methods=['GET', 'POST'])
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.website = form.website.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash(u'你的资料已经更新。')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.website.data = current_user.website
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)

@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.website = form.website.data
        user.about_me = form.about_me.data
        db.session.add(current_user)
        flash(u'资料已经更新。')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role
    form.name.data = user.name
    form.location.data = user.location
    form.website.data = user.website
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)


@main.route('/create-tag', methods=['GET', 'POST'])
def tag():
    flash(u'目前只是测试阶段，仅支持标签云相册，暂不提供永久存储。不好意思>_<')
    form = TagForm()
    app = current_app._get_current_object()
    if form.validate_on_submit():
        title = form.title.data
        sub_title = form.sub_title.data
        theme = form.theme.data
        pro_attachment = request.files.getlist('pro_attachment1')
        for upload in pro_attachment:
            filename = upload.filename.rsplit("/")[0]
            destination = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], filename)
            print "Accept incoming file:", filename
            print "Save it to:", destination
            upload.save(destination)
        # glue()
        return render_template('tag_album.html', title=title, sub_title=sub_title)
    return render_template('create/tag.html', form=form)


@main.route('/create-wall', methods=['GET', 'POST'])
def wall():
    form = WallForm()
    from flask_uploads import UploadSet, configure_uploads, IMAGES
    app = current_app._get_current_object()
    photos = UploadSet('photos', IMAGES)
    if form.validate_on_submit(): # current_user.can(Permission.CREATE_ALBUMS) and
        if request.method == 'POST' and 'photo' in request.files:
            filename=[]
            for img in request.files.getlist('photo'):
                photos.save(img)
                url = photos.url(img.filename)
                filename.append(url.replace("%20", "_"))
        title = form.title.data
        about = form.about.data
        author = current_user._get_current_object()
        album = Album(title=title,
        about=about, cover=filename[0], type=1,
        author = current_user._get_current_object())
        db.session.add(album)

        for file in filename:
            photo = Photo(path=file, album=album)
            db.session.add(photo)
        db.session.commit()
        return redirect(url_for('.album', id=album.id))
    return render_template('create/wall.html', form=form)

@main.route('/create-normal', methods=['GET', 'POST'])
@login_required
def normal():
    from flask_uploads import UploadSet, configure_uploads, IMAGES
    app = current_app._get_current_object()
    photos = UploadSet('photos', IMAGES)
    form = NormalForm()
    if form.validate_on_submit(): # current_user.can(Permission.CREATE_ALBUMS) and
        if request.method == 'POST' and 'photo' in request.files:
            filename=[]
            for img in request.files.getlist('photo'):
                photos.save(img)
                url = photos.url(img.filename)
                url = url.replace("%20", "_")
                url = url.replace("%28", "")
                url = url.replace("%29", "")
                filename.append(url)
        title = form.title.data
        about = form.about.data
        author = current_user._get_current_object()
        album = Album(title=title,
        about=about, cover=filename[0],
        author = current_user._get_current_object())
        db.session.add(album)

        for file in filename:
            photo = Photo(path=file, album=album)
            db.session.add(photo)
        db.session.commit()
        return redirect(url_for('.album', id=album.id))
    return render_template('create/normal.html', form=form)

@main.route('/like/<id>')
@login_required
#@permission_required(Permission.FOLLOW)# todo follow > like
def like(id):
    photo = Photo.query.filter_by(id=id).first()
    album = photo.album_id
    if photo is None:
        flash(u'无效的图片。')
        return redirect(url_for('.album', id=album))
    if current_user.is_like(photo):
        current_user.unlike(photo)
        return (''), 204
    current_user.like(photo)
    return (''), 204


@main.route('/base', methods=['GET','POST'])
def test():
    name = None
    form = TESTForm()

    if form.validate_on_submit():
        name = form.name.data
        session['name'] = form.name.data
        return redirect(url_for('base'))

    return render_template('test.html', form=form)

#filename = photos.save(request.files['photo'])