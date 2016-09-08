# -*-coding: utf-8-*-
from flask_wtf import Form
from wtforms import StringField, SubmitField, RadioField, PasswordField, BooleanField, FileField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo


class TagForm(Form):
    title = StringField(u'标题', validators=[Required()])
    sub_title = StringField(u'副标题')
    theme = RadioField(
        u'选择一个主题',
        choices=[('1', u'黑底白字'), ('2', u'白底黑字'), ('3', u'紫底白字')]
    )
    photos = FileField(u'选择图片')
    submit = SubmitField(u'提交')

class WallForm(Form):
    title = StringField(u'标题')
    sub_title = StringField(u'副标题')
    theme = RadioField(
        u'选择一个主题',
        choices=[('1', u'黑底白字'), ('2', u'白底黑字'), ('3', u'紫底白字')]
    )
    photos = FileField(u'选择图片')
    submit = SubmitField(u'提交')

class NormalForm(Form):
    title = StringField(u'标题')
    sub_title = StringField(u'副标题')
    theme = RadioField(
        u'选择一个主题',
        choices=[('1', u'黑底白字'), ('2', u'白底黑字'), ('3', u'紫底白字')]
    )
    photos = FileField(u'选择图片')
    submit = SubmitField(u'提交')