#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Views for the root of the app."""


from flask import render_template, request, redirect, url_for, session
from flask.views import MethodView

from brainyserver import app
from brainyserver.forms import RegisterForm, LoginForm
from brainyserver.mongodb import Researcher


@app.route('/')
def index():
    return render_template('base.html')


class Register(MethodView):
    
    form = RegisterForm
    
    def get_context(self):
        form = self.form(request.form)

        context = {'form': form}
        return context
    
    def get(self):
        context = self.get_context()
        return render_template('register.html', **context)
    
    def post(self):
        context = self.get_context()
        form = context.get('form')
        
        if form.validate():
            r = Researcher(username=form.username.data, email=form.email.data)
            r.set_password(form.password.data)
            r.save()
            session['username'] = r.username
            return redirect(url_for('index'))

        return render_template('register.html', **context)


app.add_url_rule('/register', view_func=Register.as_view('register'))


class Login(MethodView):
    
    form = LoginForm
    
    def get_context(self):
        form = self.form(request.form)

        context = {'form': form}
        return context
    
    def get(self):
        context = self.get_context()
        return render_template('login.html', **context)
    
    def post(self):
        context = self.get_context()
        form = context.get('form')
        
        if 'username' in session:
            # TODO: flash an 'already logged in' message here
            return redirect(url_for('index'))
        
        if form.validate():
            r = Researcher.objects(username=form.username_email.data).first()
            if not r:
                r = Researcher.objects(email=form.username_email.data).first()
                if not r:
                    form.username_email.errors += ('Username or '
                                                   'Email not found',)
                    return render_template('login.html', **context)
            
            if not r.check_password(form.password.data):
                form.password.errors += ('Invalid password',)
                return render_template('login.html', **context)
            
            session['username'] = r.username
            return redirect(url_for('index'))
        
        return render_template('login.html', **context)


app.add_url_rule('/login', view_func=Login.as_view('login'))


@app.route('/logout')
def logout():
    # TODO: flash a 'logged out' message here
    session.pop('username', None)
    return redirect(url_for('index'))
