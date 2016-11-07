# -*-coding: utf-8-*-
from flask_wtf import Form
from wtforms import StringField, SubmitField, RadioField, PasswordField, BooleanField, FileField, \
                    TextAreaField, SelectField, IntegerField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo, URL, Optional, NumberRange
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_uploads import UploadSet, configure_uploads, IMAGES
from wtforms.widgets import TextArea

photos = UploadSet('photos', IMAGES)

from ..models import User, Role


class EditProfileForm(Form):
    name = StringField(u'姓名或昵称', validators=[Length(0, 64)])
    status = StringField(u'签名档', validators=[Length(0, 64)])
    location = StringField(u'城市', validators=[Length(0,64)])
    website = StringField(u'网站', validators=[Length(0,64), Optional(),
                         ],
                          render_kw={"placeholder": "http://..."})
    submit = SubmitField(u'提交')

    def validate_website(self, field):
        if field.data[:4] != "http":
            print field.data[:4]
            field.data="http://"+field.data


class EditProfileAdminForm(Form):
    email = StringField(u'邮箱', validators=[Required(message= u'邮件不能为空'), Length(1, 64),
                                           Email(message= u'请输入有效的邮箱地址，比如：username@domain.com')])
    username = StringField(u'用户名', validators=[Required(message= u'用户名不能为空'), Length(1, 64),
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
    body = TextAreaField(u'留言', validators=[Required(u'内容不能为空！')], render_kw={'rows': 5})
    submit = SubmitField(u'提交')


class NewAlbumForm(Form):
    title = StringField(u'标题')
    about = TextAreaField(u'介绍', render_kw={'rows': 8})
    photo = FileField(u'图片', validators=[
        FileRequired(),
        FileAllowed(photos, u'只能上传图片！')
    ])
    asc_order = SelectField(u'显示顺序',
                            choices=[('True', u'按上传时间倒序排列'), ('False', u'按上传时间倒序排列')])
    is_public = BooleanField(u'私密相册（右侧滑出信息提示：勾选后相册仅自己可见）')
    can_comment = BooleanField(u'允许评论', render_kw={'checked': True})
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
                             choices=[('True', u'按上传时间倒序排列'), ('False', u'按上传时间倒序排列')])
    is_public = BooleanField(u'私密相册（右侧滑出信息提示：勾选后相册仅自己可见）')
    can_comment = BooleanField(u'允许评论')
    submit = SubmitField(u'提交')

class GuessNumberForm(Form):
    number = IntegerField(u'输入数字：', validators=[Required(u'数字不能为空！'), NumberRange(0, 1000, u'请输入0~1000以内的数字！')])
    submit = SubmitField(u'提交')