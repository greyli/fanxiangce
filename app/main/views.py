# -*-coding: utf-8-*-
import os
from datetime import datetime
from flask import render_template, session, redirect, \
    url_for, flash, abort, request, current_app
from flask_login import login_required, current_user
from werkzeug import secure_filename


from . import main
from .forms import TagForm, WallForm, NormalForm, EditProfileForm, EditProfileAdminForm, TESTForm, TEST2Form,  CommentForm
from .. import db
from ..models import User, Role, Permission, Album, Photo, Comment, Follow, LikePhoto, LikeAlbum, Message
from tag import glue
from wall import wall
from ..decorators import admin_required, permission_required



@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@main.route('/user/<username>', methods=['GET', 'POST'])
def user(username):
    user = User.query.filter_by(username=username).first()
    form = CommentForm()
    if user is None:
        abort(404)
    albums = user.albums.order_by(Album.timestamp.desc()).all()
    album_count = len(albums)
    photo_count = sum([len(album.photos.order_by(Photo.timestamp.asc()).all()) for album in albums])
    photo_likes = user.photo_likes.order_by(LikePhoto.timestamp.desc()).all()
    album_likes = user.album_likes.order_by(LikeAlbum.timestamp.desc()).all()
    photo_likes = [{'photo': like.like_photo, 'timestamp': like.timestamp, 'path': like.like_photo.path} for like in
                   photo_likes[:2]]
    album_likes = [{'album': like.like_album, 'photo': like.like_album.photos,
                    'timestamp': like.timestamp, 'cover': like.like_album.cover} for like in album_likes[:2]]

    if form.validate_on_submit() and current_user.is_authenticated:
        comment = Message(body=form.body.data,
                          user=user,
                          author=current_user._get_current_object())
        db.session.add(comment)
        flash(u'你的评论已经发表。')
        return redirect(url_for('.user', username=username))
    comments = user.messages.order_by(Message.timestamp.asc()).all()
    return render_template('user.html', form=form, user=user, photo_likes=photo_likes, album_likes=album_likes,
                           albums=albums, comments=comments, album_count=album_count, photo_count=photo_count)


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
    photo_likes = user.photo_likes.order_by(LikePhoto.timestamp.desc()).all()
    album_likes = user.album_likes.order_by(LikeAlbum.timestamp.desc()).all()
    photo_likes = [{'photo': like.like_photo, 'timestamp': like.timestamp, 'path':like.like_photo.path} for like in photo_likes]
    album_likes = [{'album': like.like_album, 'photo': like.like_album.photos,
                    'timestamp': like.timestamp, 'cover':like.like_album.cover} for like in album_likes]
    return render_template('likes.html', user=user, photo_likes=photo_likes, album_likes=album_likes)

@main.route('/album/<int:id>')
def album(id):
    album = Album.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    pagination = album.photos.order_by(Photo.timestamp.asc()).paginate(
        page, per_page=20, error_out=False
    )
    photos = pagination.items

    if current_user.is_authenticated:
        user = User.query.filter_by(username=current_user.username).first()
        likes = user.photo_likes.order_by(LikePhoto.timestamp.desc()).all()
        likes = [{'id': like.like_photo, 'timestamp': like.timestamp, 'path': like.like_photo.path} for like in likes]
        like_list = [like['path'] for like in likes]
    else:
        likes = ""
        like_list = []

    is_liked = album.is_liked_by(current_user)

    if album.type == 1:
        files = []
        for photo in photos:
            files.append(photo.path)
        html = wall()
        return render_template('wall.html', album=album, html=html)
    return render_template('album.html', album=album, photos=photos, pagination=pagination,
                           like_list=like_list, likes=likes, is_liked=is_liked)


@main.route('/photo/<int:id>', methods=['GET', 'POST'])
def photo(id):
    photo = Photo.query.get_or_404(id)
    album = photo.album
    form = CommentForm()
    photo_index = [p.id for p in album.photos.order_by(Photo.timestamp.asc())].index(photo.id) + 1
    #index = [i for i in xrange(len(album.photos))]
    page = request.args.get('page', photo_index, type=int)
    pagination = album.photos.order_by(Photo.timestamp.asc()).paginate(
        page, per_page=1, error_out=False
    )
    photos = pagination.items

    if current_user.is_authenticated:
        user = User.query.filter_by(username=current_user.username).first()
        likes = user.photo_likes.order_by(LikePhoto.timestamp.desc()).all()
        likes = [{'id': like.like_photo, 'timestamp': like.timestamp, 'path': like.like_photo.path, 'liked':like.photo_liked} for like in likes]
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
        return redirect(url_for('.photo', id=photo.id))
    comments = photo.comments.order_by(Comment.timestamp.asc()).all()
    return render_template('photo.html', form=form, album=album, photos=photos,
                           like_list=like_list, pagination=pagination,
                           comments=comments, photo_index=photo_index)


@main.route('/edit-profile', methods=['GET', 'POST'])
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.status = form.status.data
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
            photo = Photo(path=file, album=album,
                          author=current_user._get_current_object())
            db.session.add(photo)
        db.session.commit()
        return redirect(url_for('.album', id=album.id))
    return render_template('create/normal.html', form=form)

# @main.route('/edit-album/<int:id>')
# def edit_album(id):
#     album = Album.query.filter_by(id=id).first()
#     form = EditAlbumForm()
#     if form.validate_on_submit():
#         title = form.title.data
#         about = form.about.data
#         private = form.private.data
#         comment = form.comment.data
#     form.title.data = album.title
#     form.about.data = album.about
#     form.private.data = album.private
#     form.comment.data = album.comment




@main.route('/follow/<username>')
@login_required
# @permission_required(Permission.FOLLOW)
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if current_user.is_following(user):
        flash('You are already following this user.')
        return redirect(url_for('.user', username=username))
    current_user.follow(user)
    flash('You are now following %s.' % username)
    return redirect(url_for('.user', username=username))


@main.route('/unfollow/<username>')
@login_required
# @permission_required(Permission.FOLLOW)
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if not current_user.is_following(user):
        flash('You are not following this user.')
        return redirect(url_for('.user', username=username))
    current_user.unfollow(user)
    flash('You are not following %s anymore.' % username)
    return redirect(url_for('.user', username=username))


@main.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(
        page, per_page=10 ,#current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
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
        flash('Invalid user.')
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
#@permission_required(Permission.FOLLOW)# todo follow > like
def like_photo(id):
    photo = Photo.query.filter_by(id=id).first()
    album = photo.album
    if photo is None:
        flash(u'无效的图片。')
        return redirect(url_for('.album', id=album))
    if current_user.is_like_photo(photo):
        current_user.unlike_photo(photo)
        redirect(url_for('.photo', id=id))
    else:
        current_user.like_photo(photo)
    return redirect(url_for('.photo', id=id))

@main.route('/album/like/<id>')
@login_required
#@permission_required(Permission.FOLLOW)# todo follow > like
def like_album(id):
    album = Album.query.filter_by(id=id).first()
    if album is None:
        flash(u'无效的相册。')
        return redirect(url_for('.albums', username=album.author.username))
    if current_user.is_like_album(album):
        current_user.unlike_album(album)
        flash(u'喜欢已取消。')
        redirect(url_for('.album', id=id))
    else:
        current_user.like_album(album)
        flash(u'相册已经添加到你的喜欢里了。')
    return redirect(url_for('.album', id=id))

@main.route('/photo/unlike/<id>')
@login_required
#@permission_required(Permission.FOLLOW)# todo follow > like
def unlike_photo(id):
    photo = Photo.query.filter_by(id=id).first()
    if photo is None:
        flash(u'无效的图片。')
        return redirect(url_for('.likes', username=current_user.username))
    if current_user.is_like_photo(photo):
        current_user.unlike_photo(photo)
    return (''), 204

@main.route('/album/unlike/<id>')
@login_required
#@permission_required(Permission.FOLLOW)# todo follow > like
def unlike_album(id):
    album = Album.query.filter_by(id=id).first()
    if album is None:
        flash(u'无效的相册。')
        return redirect(url_for('.likes', username=current_user.username))
    if current_user.is_like_album(album):
        current_user.unlike_album(album)
    return (''), 204

def redirect_url(default='index'):
    return request.args.get('next') or \
           request.referrer or \
           url_for(default)

# usage: return redirect(redirect_url())

@main.route('/delete/photo/<id>')
@login_required
#@permission_required(Permission.FOLLOW)# todo follow > like
def delete_photo(id):
    photo = Photo.query.filter_by(id=id).first()
    album = photo.album
    if photo is None:
        flash(u'无效的操作。')
        return redirect(url_for('.index', username=current_user.username))
    if current_user.username != photo.author.username:
        abort(403)
    db.session.delete(photo)
    db.session.commit()
    flash(u'删除成功。')
    return redirect(url_for('.album', id=album.id))

@main.route('/delete/album/<id>')
@login_required
#@permission_required(Permission.FOLLOW)# todo follow > like
def delete_album(id):
    album = Album.query.filter_by(id=id).first()
    if album is None:
        flash(u'无效的操作。')
        return redirect(url_for('.index', username=current_user.username))
    if current_user.username != album.author.username:
        abort(403)
    db.session.delete(album)
    db.session.commit()
    flash(u'删除成功。')
    return redirect(url_for('.albums', username=album.author.username))


@main.route('/base', methods=['GET','POST'])
def test():
    name = None
    form1 = TESTForm()
    form2 = TEST2Form()

    if form1.submit1.data and form1.validate_on_submit():
        print form1.submit1.data
        name = form1.name.data
        print "hi"
        print name
        return redirect(url_for('.index'))
    print "here"
    if form2.submit2.data and form2.validate_on_submit():
        #print form2.submit.data
        name = form2.name.data
        print "ho"
        print name
        return redirect(url_for('.index'))
    return render_template('test.html', form1=form1, form2=form2)

#filename = photos.save(request.files['photo'])