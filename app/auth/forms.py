# -*- coding: utf-8 -*-
__author__ = 'lihui'
from flask_wtf import Form
from wtforms import StringField, SubmitField, RadioField, PasswordField, BooleanField, FileField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError

from ..models import User

class LoginForm(Form):
    email = StringField(u'邮箱', validators=[Required(), Length(1, 64),
                                           Email()])
    password = PasswordField(u'密码', validators=[Required()])
    remember_me = BooleanField(u'记住我')
    submit = SubmitField(u'登录')

class RegisterForm(Form):
    email = StringField(u'邮箱', validators=[Required(), Length(1, 64),
                                           Email()])
    username = StringField(u'用户名', validators=[Required(), Length(1, 64),
                                           Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                  u'用户名只能有字母，'
                                                    u'数字，点和下划线组成。')])
    password = PasswordField(u'密码', validators=[Required(),
                                                EqualTo('password2', message=u'密码必须相等')])
    password2 = PasswordField(u'确认密码', validators=[Required()])
    submit = SubmitField(u'注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(u'邮箱已经注册，请直接登录。')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(u'用户名已被注册，换一个吧。')