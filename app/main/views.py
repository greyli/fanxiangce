# -*-coding: utf-8-*-
import os
import time
import bleach
import PIL
import hashlib

from PIL import Image
from flask import render_template, redirect, \
    url_for, flash, abort, request, current_app, send_from_directory
from flask_login import login_required, current_user

from . import main
from .forms import NewAlbumForm, EditProfileAdminForm, \
    CommentForm, EditAlbumForm, AddPhotoForm, SettingForm
from .. import db, photos
from ..models import User, Role, Permission, Album, Photo, Comment,\
    Follow, LikePhoto, LikeAlbum, Message
from ..decorators import admin_required, permission_required


@main.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        photos = current_user.followed_photos
        photos  = [photo for photo in photos if photo.album.no_public == False]
    else:
        photos = ""
    return render_template('index.html', photos=photos)


@main.route('/about')
def about():
    return render_template('about.html')


@main.route('/return-files', methods=['GET'])
def return_file():
    return send_from_directory(directory='static', filename='styles.css', as_attachment=True)


@main.route('/explore', methods=['GET', 'POST'])
def explore():
    photos = Photo.query.order_by(Photo.timestamp.desc()).all()
    photos = [photo for photo in photos if photo.album.no_public == False and photo.author != current_user]
    photo_type = "new"
    return render_template('explore.html', photos=photos, type=photo_type)


@main.route('/explore/hot', methods=['GET', 'POST'])
def explore_hot():
    photos = Photo.query.all()
    photos = [photo for photo in photos if photo.album.no_public == False]
    result = {}
    for photo in photos:
        result[photo] = len(list(photo.photo_liked))
    sorted_photo = sorted(result.items(), key=lambda x: x[1], reverse=True)
    temp = []
    for photo in sorted_photo:
        temp.append(photo[0])
    photo_type = "hot"
    return render_template('explore.html', photos=temp, type=photo_type)


@main.route('/edit-photo/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_photo(id):
    album = Album.query.get_or_404(id)
    photos = album.photos.order_by(Photo.order.asc())
    if request.method == 'POST':
        for photo in photos:
            photo.about = request.form[str(photo.id)]
            photo.order = request.form["order-" + str(photo.id)]
            db.session.add(photo)
        album.cover = request.form['cover']
        db.session.add(album)
        db.session.commit()
        flash(u'更改已保存。', 'success')
        return redirect(url_for('.album', id=id))
    enu_photos = []
    for index, photo in enumerate(photos):
        enu_photos.append((index, photo))

    return render_template('edit_photo.html', album=album, photos=photos, enu_photos=enu_photos)


@main.route('/fast-sort/<int:id>', methods=['GET', 'POST'])
@login_required
def fast_sort(id):
    album = Album.query.get_or_404(id)
    photos = album.photos.order_by(Photo.order.asc())
    enu_photos = []
    for index, photo in enumerate(photos):
        enu_photos.append((index, photo))
    return render_template('fast_sort.html', album=album, photos=photos, enu_photos=enu_photos)


@main.route('/edit-album/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_album(id):
    album = Album.query.get_or_404(id)
    form = EditAlbumForm()
    if form.validate_on_submit():
        album.title = form.title.data
        album.about = form.about.data
        album.asc_order = form.asc_order.data
        album.no_public = form.no_public.data
        album.no_comment = form.no_comment.data
        album.author = current_user._get_current_object()
        flash(u'更改已保存。', 'success')
        return redirect(url_for('.album', id=id))
    form.title.data = album.title
    form.about.data = album.about
    form.asc_order.data = album.asc_order
    form.no_comment.data = album.no_comment
    form.no_public.data = album.no_public
    return render_template('edit_album.html', form=form, album=album)


@main.route('/save-edit/<int:id>', methods=['GET', 'POST'])
@login_required
def save_edit(id):
    album = Album.query.get_or_404(id)
    photos = album.photos
    for photo in photos:
        photo.about = request.form[str(photo.id)]
        photo.order = request.form["order-" + str(photo.id)]
        db.session.add(photo)
    default_value = album.cover
    album.cover = request.form.get('cover', default_value)
    db.session.add(album)
    db.session.commit()
    flash(u'更改已保存。', 'success')
    return redirect(url_for('.album', id=id))


@main.route('/save-photo-edit/<int:id>', methods=['GET', 'POST'])
@login_required
def save_photo_edit(id):
    photo = Photo.query.get_or_404(id)
    album = photo.album
    photo.about = request.form.get('about', '')
    # set default_value to avoid 400 error.
    default_value = album.cover
    print default_value
    album.cover = request.form.get('cover', default_value)
    db.session.add(photo)
    db.session.add(album)
    db.session.commit()
    flash(u'更改已保存。', 'success')
    return redirect(url_for('.photo', id=id))


@main.route('/save-sort/<int:id>', methods=['GET', 'POST'])
@login_required
def save_sort(id):
    album = Album.query.get_or_404(id)
    photos = album.photos
    for photo in photos:
        photo.order = request.form["order-" + str(photo.id)]
        db.session.add(photo)
    db.session.commit()
    flash(u'更改已保存。', 'success')
    return redirect(url_for('.album', id=id))


@main.route('/<username>', methods=['GET', 'POST'])
def albums(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)

    page = request.args.get('page', 1, type=int)
    pagination = user.albums.order_by(Album.timestamp.desc()).paginate(
            page, per_page=current_app.config['FANXIANGCE_ALBUMS_PER_PAGE'], error_out=False)
    albums = pagination.items

    photo_count = sum([len(album.photos.all()) for album in albums])
    album_count = len(albums)

    allowed_tags = ['br']
    if user.about_me:
        about_me = bleach.linkify(bleach.clean(
            user.about_me.replace('\r', '<br>'), tags=allowed_tags, strip=True))
    else:
        about_me = None
    form = CommentForm()
    if form.validate_on_submit() and current_user.is_authenticated:
        comment = Message(body=form.body.data,
                          user=user,
                          author=current_user._get_current_object())
        db.session.add(comment)
        flash(u'你的评论已经发表。', 'success')
        return redirect(url_for('.albums', username=username))

    comments = user.messages.order_by(Message.timestamp.asc()).all()
    return render_template('albums.html', form=form, comments=comments,
                           user=user, albums=albums, album_count=album_count,
                           photo_count=photo_count, pagination=pagination,
                           about_me=about_me)


@main.route('/<username>/likes')
def likes(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    if current_user!= user and not user.like_public:
       return render_template('like_no_public.html', user=user)
    page = request.args.get('page', 1, type=int)
    pagination = user.photo_likes.order_by(LikePhoto.timestamp.desc()).paginate(
        page, per_page=current_app.config['FANXIANGCE_PHOTO_LIKES_PER_PAGE'], error_out=False)
    photo_likes = pagination.items
    photo_likes = [{'photo': like.like_photo, 'timestamp': like.timestamp, 'url_t':like.like_photo.url_t} for like in photo_likes]
    type = "photo"
    return render_template('likes.html', user=user, photo_likes=photo_likes,
                           pagination=pagination, type=type)


@main.route('/<username>/likes/album')
def album_likes(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    if current_user!= user and not user.like_public:
       return render_template('like_no_public.html', user=user)
    page = request.args.get('page', 1, type=int)
    pagination = user.album_likes.order_by(LikeAlbum.timestamp.desc()).paginate(
        page, per_page=current_app.config['FANXIANGCE_ALBUM_LIKES_PER_PAGE'], error_out=False)
    album_likes = pagination.items
    album_likes = [{'album': like.like_album, 'photo': like.like_album.photos,
                    'timestamp': like.timestamp, 'cover':like.like_album.cover} for like in album_likes]
    type = "album"
    return render_template('likes.html', user=user, album_likes=album_likes,
                           pagination=pagination, type=type)


@main.route('/album/<int:id>')
def album(id):
    album = Album.query.get_or_404(id)
    # display default cover when an album is empty
    placeholder = 'http://p1.bpimg.com/567591/15110c0119201359.png'
    photo_amount = len(list(album.photos))
    if photo_amount == 0:
        album.cover = placeholder
    elif photo_amount != 0 and album.cover == placeholder:
        album.cover = album.photos[0].path

    if current_user != album.author and album.no_public == True:
        abort(404)
    page = request.args.get('page', 1, type=int)
    if album.asc_order:
        pagination = album.photos.order_by(Photo.order.asc()).paginate(
            page, per_page=current_app.config['FANXIANGCE_PHOTOS_PER_PAGE'],
            error_out=False)
    else:
        pagination = album.photos.order_by(Photo.order.asc()).paginate(
            page, per_page=current_app.config['FANXIANGCE_PHOTOS_PER_PAGE'],
            error_out=False)
    photos = pagination.items
    if len(photos) == 0:
        no_pic = True
    else:
        no_pic = False
    if current_user.is_authenticated:
        user = User.query.filter_by(username=current_user.username).first()
        likes = user.photo_likes.order_by(LikePhoto.timestamp.asc()).all()
        likes = [{'id': like.like_photo, 'timestamp': like.timestamp, 'url_t': like.like_photo.url_t} for like in likes]
    else:
        likes = ""

    return render_template('album.html', album=album, photos=photos, pagination=pagination,
                           likes=likes, no_pic=no_pic)


@main.route('/photo/<int:id>', methods=['GET', 'POST'])
def photo(id):
    photo = Photo.query.get_or_404(id)
    album = photo.album
    if current_user != album.author and album.no_public == True:
        abort(404)

    photo_sum = len(list(album.photos))
    form = CommentForm()
    photo_index = [p.id for p in album.photos.order_by(Photo.order.asc())].index(photo.id) + 1
    if current_user.is_authenticated:
        user = User.query.filter_by(username=current_user.username).first()
        likes = user.photo_likes.order_by(LikePhoto.timestamp.desc()).all()
        likes = [{'id': like.like_photo, 'timestamp': like.timestamp, 'url': like.like_photo.url, 'liked':like.photo_liked} for like in likes]
    else:
        likes = ""

    if form.validate_on_submit():
        if current_user.is_authenticated:
            comment = Comment(body=form.body.data,
                              photo=photo,
                              author=current_user._get_current_object())
            db.session.add(comment)
            flash(u'你的评论已经发表。', 'success')
            return redirect(url_for('.photo', id=photo.id))
        else:
            flash(u'请先登录。', 'info')
    page = request.args.get('page', 1, type=int)
    pagination = photo.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=current_app.config['FANXIANGCE_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    amount = len(comments)
    return render_template('photo.html', form=form, album=album, amount=amount,
                           photo=photo, pagination=pagination,
                           comments=comments, photo_index=photo_index, photo_sum=photo_sum)


@main.route('/photo/n/<int:id>')
def photo_next(id):
    "redirect to next imgae"
    photo_now = Photo.query.get_or_404(id)
    album = photo_now.album
    photos = album.photos.order_by(Photo.order.asc())
    position = list(photos).index(photo_now) + 1
    if position == len(list(photos)):
        flash(u'已经是最后一张了。', 'info')
        return redirect(url_for('.photo', id=id))
    photo = photos[position]
    return redirect(url_for('.photo', id=photo.id))


@main.route('/photo/p/<int:id>')
def photo_previous(id):
    "redirect to previous imgae"
    photo_now = Photo.query.get_or_404(id)
    album = photo_now.album
    photos = album.photos.order_by(Photo.order.asc())
    position = list(photos).index(photo_now) - 1
    if position == -1:
        flash(u'已经是第一张了。', 'info')
        return redirect(url_for('.photo', id=id))
    photo = photos[position]
    return redirect(url_for('.photo', id=photo.id))


@main.route('/setting', methods=['GET', 'POST'])
@login_required
def setting():
    form = SettingForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.status = form.status.data
        current_user.location = form.location.data
        current_user.website = form.website.data
        current_user.about_me = form.about_me.data
        current_user.like_public = form.like_public.data
        flash(u'你的设置已经更新。', 'success')
        return redirect(url_for('.albums', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.status.data = current_user.status
    form.website.data = current_user.website
    form.about_me.data = current_user.about_me
    form.like_public.data = current_user.like_public
    return render_template('setting.html', form=form, user=current_user)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    return redirect(url_for('.setting') + '#profile')


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
        flash(u'资料已经更新。', 'success')
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


@main.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOADED_PHOTOS_DEST'],
                               filename)

# add different suffix for image
img_suffix = {
    300: '_t',  # thumbnail
    800: '_s'  # show
}


def image_resize(image, base_width):
    #: create thumbnail
    filename, ext = os.path.splitext(image)
    img = Image.open(photos.path(image))
    if img.size[0] <= base_width:
        return photos.url(image)
    w_percent = (base_width / float(img.size[0]))
    h_size = int((float(img.size[1]) * float(w_percent)))
    img = img.resize((base_width, h_size), PIL.Image.ANTIALIAS)
    img.save(os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], filename + img_suffix[base_width] + ext))
    return url_for('.uploaded_file', filename=filename + img_suffix[base_width] + ext)


def save_image(files):
    photo_amount = len(files)
    if photo_amount > 50:
        flash(u'抱歉，测试阶段每次上传不超过50张！', 'warning')
        return redirect(url_for('.new_album'))
    images = []
    for img in files:
        filename = hashlib.md5(current_user.username + str(time.time())).hexdigest()[:10]
        image = photos.save(img, name=filename + '.')
        file_url = photos.url(image)
        url_s = image_resize(image, 800)
        url_t = image_resize(image, 300)
        images.append((file_url, url_s, url_t))
    return images


@main.route('/new-album', methods=['GET', 'POST'])
@login_required
def new_album():
    form = NewAlbumForm()
    if form.validate_on_submit(): # current_user.can(Permission.CREATE_ALBUMS)
        if request.method == 'POST' and 'photo' in request.files:
            images = save_image(request.files.getlist('photo'))

        title = form.title.data
        about = form.about.data
        author = current_user._get_current_object()
        no_public = form.no_public.data
        no_comment = form.no_comment.data
        album = Album(title=title, about=about,
                      cover=images[0][2], author=author,
                      no_public=no_public, no_comment=no_comment)
        db.session.add(album)

        for url in images:
            photo = Photo(url=url[0], url_s=url[1], url_t=url[2],
                          album=album, author=current_user._get_current_object())
            db.session.add(photo)
        db.session.commit()
        flash(u'相册创建成功！', 'success')
        return redirect(url_for('.edit_photo', id=album.id))
    return render_template('new_album.html', form=form)


@main.route('/add-photo/<int:id>', methods=['GET', 'POST'])
@login_required
def add_photo(id):
    album = Album.query.get_or_404(id)
    form = AddPhotoForm()
    if form.validate_on_submit(): # current_user.can(Permission.CREATE_ALBUMS)
        if request.method == 'POST' and 'photo' in request.files:
            images = save_image(request.files.getlist('photo'))

            for url in images:
                photo = Photo(url=url[0], url_s=url[1], url_t=url[2],
                              album=album, author=current_user._get_current_object())
                db.session.add(photo)
            db.session.commit()
        flash(u'图片添加成功！', 'success')
        return redirect(url_for('.album', id=album.id))
    return render_template('add_photo.html', form=form, album=album)


@main.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    return render_template('upload.html')


@main.route('/upload-add', methods=['GET', 'POST'])
@login_required
def upload_add():
    id = request.form.get('album')
    return redirect(url_for('.add_photo', id=id))


@main.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(u'操作无效。', 'warning')
        return redirect(url_for('.index'))
    if current_user.is_following(user):
        flash(u'你已经关注过该用户了。', 'warning')
        return redirect(url_for('.alubms', username=username))
    current_user.follow(user)
    flash(u'成功关注%s。' % user.name, 'info')
    return redirect(url_for('.albums', username=username))


@main.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(u'操作无效。', 'warning')
        return redirect(url_for('.index'))
    if not current_user.is_following(user):
        flash(u'你没有关注该用户。', 'warning')
        return redirect(url_for('.alubms', username=username))
    current_user.unfollow(user)
    flash(u'取消关注%s。' % user.name, 'info')
    return redirect(url_for('.albums', username=username))


@main.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(u'操作无效。', 'warning')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(
        page, per_page=current_app.config['FANXIANGCE_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.follower, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title=u"的关注者",
                           endpoint='.followers', pagination=pagination,
                           follows=follows)


@main.route('/followed-by/<username>')
def followed_by(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(u'操作无效。', 'warning')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(
        page, per_page=10, #current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.followed, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title=u"关注的人",
                           endpoint='.followed_by', pagination=pagination,
                           follows=follows)


@main.route('/photo/like/<id>')
@login_required
#@permission_required(Permission.FOLLOW)
def like_photo(id):
    photo = Photo.query.filter_by(id=id).first()
    album = photo.album
    if photo is None:
        flash(u'无效的图片。', 'warning')
        return redirect(url_for('.album', id=album))
    if current_user.is_like_photo(photo):
        current_user.unlike_photo(photo)
        photo.author.liked -= 1
        redirect(url_for('.photo', id=id))
    else:
        current_user.like_photo(photo)
        photo.author.liked += 1
    return redirect(url_for('.photo', id=id))


@main.route('/photo/unlike/<id>')
@login_required
#@permission_required(Permission.FOLLOW)
def unlike_photo(id):
    # unlike photo in likes page.
    photo = Photo.query.filter_by(id=id).first()
    if photo is None:
        flash(u'无效的图片。', 'warning')
        return redirect(url_for('.likes', username=current_user.username))
    if current_user.is_like_photo(photo):
        current_user.unlike_photo(photo)
        photo.author.liked -= 1
    return (''), 204


@main.route('/album/like/<id>')
@login_required
#@permission_required(Permission.FOLLOW)
def like_album(id):
    album = Album.query.filter_by(id=id).first()
    if album is None:
        flash(u'无效的相册。', 'warning')
        return redirect(url_for('.albums', username=album.author.username))
    if current_user.is_like_album(album):
        current_user.unlike_album(album)
        flash(u'喜欢已取消。', 'info')
        redirect(url_for('.album', id=id))
    else:
        current_user.like_album(album)
        flash(u'相册已经添加到你的喜欢里了。', 'success')
    return redirect(url_for('.album', id=id))


@main.route('/album/unlike/<id>')
@login_required
# @permission_required(Permission.FOLLOW)
def unlike_album(id):
    album = Album.query.filter_by(id=id).first()
    if album is None:
        flash(u'无效的相册。', 'warning')
        return redirect(url_for('.likes', username=current_user.username))
    if current_user.is_like_album(album):
        current_user.unlike_album(album)
    return (''), 204


@main.route('/delete/photo/<id>')
@login_required
def delete_photo(id):
    photo = Photo.query.filter_by(id=id).first()
    album = photo.album
    if photo is None:
        flash(u'无效的操作。', 'warning')
        return redirect(url_for('.index', username=current_user.username))
    if current_user.username != photo.author.username:
        abort(403)
    db.session.delete(photo)
    db.session.commit()
    flash(u'删除成功。', 'success')
    return redirect(url_for('.album', id=album.id))


@main.route('/delete/edit-photo/<id>')
@login_required
def delete_edit_photo(id):
    photo = Photo.query.filter_by(id=id).first()
    album = photo.album
    if photo is None:
        flash(u'无效的操作。', 'warning')
        return redirect(url_for('.index', username=current_user.username))
    if current_user.username != photo.author.username:
        abort(403)
    db.session.delete(photo)
    db.session.commit()
    return (''), 204


@main.route('/delete/album/<id>')
@login_required
def delete_album(id):
    album = Album.query.filter_by(id=id).first()
    if album is None:
        flash(u'无效的操作。', 'warning')
        return redirect(url_for('.index', username=current_user.username))
    if current_user.username != album.author.username:
        abort(403)
    db.session.delete(album)
    db.session.commit()
    flash(u'删除成功。', 'success')
    return redirect(url_for('.albums', username=album.author.username))