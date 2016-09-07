# -*-coding: utf-8-*-
from datetime import datetime
from flask import render_template, session, redirect, url_for

from . import main
from .forms import TagForm, LoginForm, RegisterForm
from .. import db
from tag import glue

@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', form=form)

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    return render_template('register.html', form=form)

@main.route('/new-album/tag', methods=['GET', 'POST'])
def tag():
    form = TagForm()
    if form.validate_on_submit():
        title = form.title.data
        sub_title = form.sub_title.data
        theme = form.theme.data
        glue()
        return render_template('album.html', title=title, sub_title=sub_title)
    return render_template('make.html', form=form)