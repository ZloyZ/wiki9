# -*- coding: utf-8 -*-

from wiki9 import app
from wiki9.auth import is_root, login_user, logout_user
from wiki9.utils import RedirectBackForm, redirect_back
from wiki9 import wiki

from flask import url_for, redirect, render_template, abort, flash
from flask.ext import wtf

class LoginForm(RedirectBackForm):
    login    = wtf.TextField(u"Логин", [wtf.validators.Required()])
    password = wtf.PasswordField(u"Пароль", [wtf.validators.Required()])

@app.route('/')
def index():
    return redirect(url_for('show_page', path='main'))

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if login_user(form.login.data, form.password.data):
            flash(u"Добро пожаловать", 'success')
            return redirect(url_for('index'))
        else:
            flash(u"Неверный логин или пароль", 'alert')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect_back()

@app.route('/<path:path>/')
def show_page(path='main'):
    page = wiki.get_page(path)
    if not page: abort(404)

    if page.has_key('redirect'):
        return redirect(page['redirect'])
   
    sidenav = wiki.get_page('sidenav')
    if not sidenav: sidenav = {}

    return render_template('show_page.html', sidenav=sidenav, page=page)

