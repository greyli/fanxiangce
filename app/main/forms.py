# -*-coding: utf-8-*-
from flask_wtf import Form
from wtforms import StringField, SubmitField, RadioField, PasswordField, BooleanField, FileField, \
                    TextAreaField, SelectField, IntegerField, SelectMultipleField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, URL, Optional, NumberRange
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.widgets import TextArea

from .. import photos
from ..models import User, Role


class SettingForm(Form):
    name = StringField(u'姓名或昵称', validators=[Length(0, 64)])
    status = StringField(u'签名档', validators=[Length(0, 64)])
    location = StringField(u'城市', validators=[Length(0, 64)])
    website = StringField(u'网站', validators=[Length(0, 64), Optional(),
                         ], render_kw={"placeholder": "http://..."})
    about_me = TextAreaField(u'关于我', render_kw={'rows': 8})
    like_public = BooleanField(u'公开我的喜欢')
    submit = SubmitField(u'提交')

    def validate_website(self, field):
        if field.data[:4] != "http":
             field.data = "http://" + field.data


class EditProfileAdminForm(Form):
    email = StringField(u'邮箱', validators=[DataRequired(message= u'邮件不能为空'), Length(1, 64),
                                           Email(message= u'请输入有效的邮箱地址，比如：username@domain.com')])
    username = StringField(u'用户名', validators=[DataRequired(message= u'用户名不能为空'), Length(1, 64),
                                               Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                      u'用户名只能有字母，'
                                                      u'数字，点和下划线组成。')])
    confirmed = BooleanField(u'确认状态')
    role = SelectField(u'角色', coerce=int)
    name = StringField(u'姓名或昵称', validators=[Length(0, 64)])
    location = StringField(u'城市', validators=[Length(0, 64)])
    website = StringField(u'网站', validators=[Length(0, 64),
                                             URL(message= u'请输入有效的地址，比如：http://withlihui.com')])
    about_me = TextAreaField(u'关于我')
    submit = SubmitField(u'提交')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError(u'邮箱已经注册，请直接登录。')

    def validate_username(self, field):
        if field.data != self.user.username and \
        User.query.filter_by(username=field.data).first():
            raise ValidationError(u'用户名已被注册，换一个吧。')


class CommentForm(Form):
    body = TextAreaField(u'留言', validators=[DataRequired(u'内容不能为空！')], render_kw={'rows': 5})
    submit = SubmitField(u'提交')


class NewAlbumForm(Form):
    title = StringField(u'标题')
    about = TextAreaField(u'介绍', render_kw={'rows': 8})
    photo = FileField(u'图片', validators=[
        FileRequired(u'你还没有选择图片！'),
        FileAllowed(photos, u'只能上传图片！')
    ])
    asc_order = SelectField(u'显示顺序',
                            choices=[('True', u'按上传时间倒序排列'), ('False', u'按上传时间倒序排列')])
    no_public = BooleanField(u'私密相册（勾选后相册仅自己可见）')
    no_comment = BooleanField(u'禁止评论')
    submit = SubmitField(u'提交')


class AddPhotoForm(Form):
    photo = FileField(u'图片', validators=[
        FileRequired(),
        FileAllowed(photos, u'只能上传图片！')
    ])
    submit = SubmitField(u'提交')


class EditAlbumForm(Form):
    title = StringField(u'标题')
    about = TextAreaField(u'介绍', render_kw={'rows': 8})
    asc_order = SelectField(u'显示顺序',
                             choices=[("1", u'按上传时间倒序排列'), ("0", u'按上传时间倒序排列')])
    no_public = BooleanField(u'私密相册（右侧滑出信息提示：勾选后相册仅自己可见）')
    no_comment = BooleanField(u'允许评论')
    submit = SubmitField(u'提交')

