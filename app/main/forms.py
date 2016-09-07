# -*-coding: utf-8-*-
from flask_wtf import Form
from wtforms import StringField, SubmitField, RadioField, PasswordField, BooleanField, FileField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo

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
    remember_me = BooleanField(u'记住我')
    submit = SubmitField(u'登录')

class TagForm(Form):
    title = StringField(u'标题')
    sub_title = StringField(u'副标题')
    theme = RadioField(
        u'选择一个主题',
        choices=[('1', u'黑底白字'), ('2', u'白底黑字'), ('3', u'紫底白字')]
    )
    photos = FileField(u'选择图片')
    submit = SubmitField(u'提交')