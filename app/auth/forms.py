# -*- coding: utf-8 -*-
__author__ = 'lihui'
from flask_wtf import Form
from wtforms import StringField, SubmitField, RadioField, PasswordField, BooleanField, FileField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError

from ..models import User

class LoginForm(Form):
    email = StringField(u'邮箱', validators=[Required(message= u'邮箱不能为空'), Length(1, 64),
                                           Email(message= u'请输入有效的邮箱地址，比如：username@domain.com')])
    password = PasswordField(u'密码', validators=[Required(message= u'密码不能为空')])
    remember_me = BooleanField(u'记住我')
    submit = SubmitField(u'登录')

class RegisterForm(Form):
    name = StringField(u'用户名', validators=[Required(message= u'用户名不能为空'), Length(1, 64)])
    email = StringField(u'邮箱', validators=[Required(message= u'邮箱不能为空'), Length(1, 64),
                                           Email(message= u'请输入有效的邮箱地址，比如：username@domain.com')])
    username = StringField(u'ID', validators=[Required(message= u'ID不能为空'), Length(1, 64),
                                           Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                  u'用户名只能有字母，'
                                                    u'数字，点和下划线组成。')])
    password = PasswordField(u'密码', validators=[Required(message= u'密码不能为空'),
                                                EqualTo('password2', message=u'密码必须相等')])
    password2 = PasswordField(u'确认密码', validators=[Required(message= u'密码不能为空')])
    submit = SubmitField(u'注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(u'邮箱已经注册，请直接登录。')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(u'用户名已被注册，换一个吧。')


class ChangePasswordForm(Form):
    old_password = PasswordField(u'旧密码', validators=[Required(message= u'密码不能为空')])
    password = PasswordField(u'新密码', validators=[
        Required(message= u'密码不能为空'), EqualTo('password2', message=u'密码必须匹配。')])
    password2 = PasswordField(u'确认新密码', validators=[Required(message= u'密码不能为空')])
    submit = SubmitField(u'更改')


class PasswordResetRequestForm(Form):
    email = StringField(u'邮箱', validators=[Required(message= u'邮箱不能为空'), Length(1, 64),
                                             Email(message= u'请输入有效的邮箱地址，比如：username@domain.com')])
    submit = SubmitField(u'重设密码')


class PasswordResetForm(Form):
    email = StringField(u'邮箱', validators=[Required(message= u'邮箱不能为空'), Length(1, 64),
                                             Email(message= u'请输入有效的邮箱地址，比如：username@domain.com')])
    password = PasswordField(u'新密码', validators=[
        Required(message= u'密码不能为空'), EqualTo(u'password2', message=u'密码必须匹配。')])
    password2 = PasswordField(u'确认密码', validators=[Required(message= u'密码不能为空')])
    submit = SubmitField(u'重设')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError(u'邮箱地址有错，请检查。')


class ChangeEmailForm(Form):
    email = StringField(u'新邮箱地址', validators=[Required(message= u'邮箱不能为空'), Length(1, 64),
                                                 Email(message= u'请输入有效的邮箱地址，比如：username@domain.com')])
    password = PasswordField(u'密码', validators=[Required(message= u'密码不能为空')])
    submit = SubmitField(u'更新')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(u'邮箱已经注册过了，换一个吧。')