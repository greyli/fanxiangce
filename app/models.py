# -*- coding: utf-8 -*-
import hashlib

from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, request
from datetime import datetime

from . import db
from . import login_manager


class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    CREATE_ALBUMS = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.String(64), default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.FOLLOW |
                     Permission.COMMENT |
                     Permission.CREATE_ALBUMS, True),
            'Moderator': (Permission.FOLLOW |
                          Permission.COMMENT |
                          Permission.CREATE_ALBUMS |
                          Permission.MODERATE_COMMENTS, False),
            'Administrator': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name


class LikePhoto(db.Model):
    __tablename__ = 'like_photo'
    like_photo_id = db.Column(db.Integer, db.ForeignKey('photos.id'),
                              primary_key=True)
    photo_liked_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                               primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())


class LikeAlbum(db.Model):
    __tablename__ = 'like_album'
    like_album_id = db.Column(db.Integer, db.ForeignKey('albums.id'),
                              primary_key=True)
    album_liked_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                               primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())


class Follow(db.Model):
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                            primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                            primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())


class Photo(db.Model):
    __tablename__ = 'photos'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(64))
    url_s = db.Column(db.String(64))
    url_t = db.Column(db.String(64))
    about = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    order = db.Column(db.Integer)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    album_id = db.Column(db.Integer, db.ForeignKey('albums.id'))
    photo_liked = db.relationship('LikePhoto', foreign_keys=[LikePhoto.like_photo_id],
                                  backref=db.backref('like_photo', lazy='joined'),
                                  lazy='dynamic', cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='photo', lazy='dynamic')

    def is_liked_by(self, user):
        return self.photo_liked.filter_by(
            photo_liked_id=user.id).first() is not None


class Album(db.Model):
    __tablename__ = 'albums'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    about = db.Column(db.Text)
    cover = db.Column(db.String(64))
    type = db.Column(db.Integer, default=0)
    tag = db.Column(db.String(64))
    no_public = db.Column(db.Boolean, default=True)
    no_comment = db.Column(db.Boolean, default=True)
    asc_order = db.Column(db.Boolean, default=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    photos = db.relationship('Photo', backref='album', lazy='dynamic')
    album_liked = db.relationship('LikeAlbum', foreign_keys=[LikeAlbum.like_album_id],
                                  backref=db.backref('like_album', lazy='joined'),
                                  lazy='dynamic', cascade='all, delete-orphan')

    def is_liked_by(self, user):
        return self.album_liked.filter_by(
            album_liked_id=user.id).first() is not None


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    # body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    disabled = db.Column(db.Boolean)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    photo_id = db.Column(db.Integer, db.ForeignKey('photos.id'))


class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    # body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    disabled = db.Column(db.Boolean)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    status = db.Column(db.String(64))
    liked = db.Column(db.Integer, default=0)
    password_hash = db.Column(db.String(64))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    confirmed = db.Column(db.Boolean, default=False)
    like_public = db.Column(db.Boolean, default=True)
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    website = db.Column(db.String(64))
    background = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    avatar_hash = db.Column(db.String(32))
    albums = db.relationship('Album', backref='author', lazy='dynamic')
    photos = db.relationship('Photo', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')
    messages = db.relationship('Message', backref='user', lazy='dynamic', foreign_keys='[Message.user_id]')
    message_from = db.relationship('Message', backref='author', lazy='dynamic', foreign_keys='[Message.author_id]')
    photo_likes = db.relationship('LikePhoto', foreign_keys=[LikePhoto.photo_liked_id],
                                  backref=db.backref('photo_liked', lazy='joined'),
                                  lazy='dynamic', cascade='all, delete-orphan')
    album_likes = db.relationship('LikeAlbum', foreign_keys=[LikeAlbum.album_liked_id],
                                  backref=db.backref('album_liked', lazy='joined'),
                                  lazy='dynamic', cascade='all, delete-orphan')
    followers = db.relationship('Follow', foreign_keys=[Follow.followed_id],
                                backref=db.backref('followed', lazy='joined'),
                                lazy='dynamic', cascade='all, delete-orphan')
    followed = db.relationship('Follow', foreign_keys=[Follow.follower_id],
                               backref=db.backref('follower', lazy='joined'),
                               lazy='dynamic', cascade='all, delete-orphan')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FANXIANGCE_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = hashlib.md5(
                self.email.encode('utf-8')).hexdigest()

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        self.avatar_hash = hashlib.md5(
            self.email.encode('utf-8')).hexdigest()
        db.session.add(self)
        return True

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def gravatar(self, size=100, default='identicon', rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://secure.gravatar.com/avatar'
        hash = self.avatar_hash or hashlib.md5(self.email.encode('utf-8')).hexigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)

    def can(self, permissions):
        return self.role is not None and \
               (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': self.id, 'new_email': new_email})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def follow(self, user):
        if not self.is_following(user):
            f = Follow(follower=self, followed=user)
            db.session.add(f)

    def unfollow(self, user):
        f = self.followed.filter_by(followed_id=user.id).first()
        if f:
            db.session.delete(f)

    def is_following(self, user):
        return self.followed.filter_by(
            followed_id=user.id).first() is not None

    def is_followed_by(self, user):
        return self.followers.filter_by(
            follower_id=user.id).first() is not None

    def is_friend(self, user):
        return self.followed.filter_by(
            followed_id=user.id).first() is not None and \
               self.followers.filter_by(
                   follower_id=user.id).first() is not None

    def like_photo(self, photo):
        if not self.is_like_photo(photo):
            p = LikePhoto(photo_liked=self, like_photo=photo)
            db.session.add(p)

    def like_album(self, album):
        if not self.is_like_photo(album):
            a = LikeAlbum(album_liked=self, like_album=album)
            db.session.add(a)

    def unlike_photo(self, photo):
        p = self.photo_likes.filter_by(like_photo_id=photo.id).first()
        if p:
            db.session.delete(p)

    def unlike_album(self, album):
        p = self.album_likes.filter_by(like_album_id=album.id).first()
        if p:
            db.session.delete(p)

    def is_like_photo(self, photo):
        return self.photo_likes.filter_by(like_photo_id=photo.id).first() is not None

    def is_like_album(self, album):
        return self.album_likes.filter_by(like_album_id=album.id).first() is not None

    @property
    def followed_photos(self):
        return Photo.query.join(Follow, Follow.followed_id == Photo.author_id) \
            .filter(Follow.follower_id == self.id)

    def __repr__(self):
        return '<Role %r>' % self.name


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
