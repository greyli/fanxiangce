# -*-coding: utf-8-*-
from datetime import datetime
from flask import render_template, session, redirect, url_for, flash
from flask_login import current_user

from . import main
from .forms import TagForm, WallForm, NormalForm
from .. import db
from tag import glue

@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@main.route('/create/tag', methods=['GET', 'POST'])
def tag():
    flash(u'目前只是测试阶段，仅支持标签云相册，暂不提供永久存储。不好意思>_<')
    form = TagForm()
    if form.validate_on_submit():
        title = form.title.data
        sub_title = form.sub_title.data
        theme = form.theme.data
        glue()
        return render_template('album.html', title=title, sub_title=sub_title)
    return render_template('create/tag.html', form=form)


@main.route('/create/wall', methods=['GET', 'POST'])
def wall():
    form = WallForm()
    if form.validate_on_submit():
        title = form.title.data
        sub_title = form.sub_title.data
        theme = form.theme.data
        return render_template('album.html', title=title, sub_title=sub_title)
    return render_template('create/wall.html', form=form)


@main.route('/create/normal', methods=['GET', 'POST'])
def normal():
    form = NormalForm()
    if form.validate_on_submit():
        title = form.title.data
        sub_title = form.sub_title.data
        return render_template('album.html', title=title, sub_title=sub_title)
    return render_template('create/normal.html', form=form)