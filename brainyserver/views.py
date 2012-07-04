#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Views for the root of the app."""


from flask import (render_template, request, redirect, url_for, session,
                   abort, g)
from flask.views import MethodView

from brainyserver import app
from brainyserver.forms import RegisterForm, LoginForm, AddExpAppForm
from brainyserver.mongodb import Researcher, ExpApp


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
            return redirect(url_for('user.index', username=r.username))

        return render_template('register.html', **context)


app.add_url_rule('/register', view_func=Register.as_view('register'))


class Login(MethodView):
    
    form = LoginForm
    
    def get_context(self):
        form = self.form(request.form)
        return_to = request.args.get('return_to')
        context = {'form': form, 'return_to': return_to}
        return context
    
    def get(self):
        context = self.get_context()
        g.context = context
        return render_template('login.html', **context)
    
    def post(self):
        context = self.get_context()
        g.context = context
        form = context.get('form')
        
        if 'username' in session:
            # TODO: flash an 'already logged in' message here
            return redirect(url_for('index'))
        
        if form.validate():
            r = Researcher.objects(
                        username=form.username_email.data).first()
            if not r:
                r = Researcher.objects(
                        email=form.username_email.data).first()
                if not r:
                    form.username_email.errors += ('Username or '
                                                   'Email not found',)
                    return render_template('login.html', **context)
            
            if not r.check_password(form.password.data):
                form.password.errors += ('Invalid password',)
                return render_template('login.html', **context)
            
            session['username'] = r.username
            if context['return_to'] is None:
                redir_url = url_for('user.index', username=r.username)
            else:
                redir_url = context['return_to']
            return redirect(redir_url)
        
        return render_template('login.html', **context)


app.add_url_rule('/login', view_func=Login.as_view('login'))


@app.route('/logout')
def logout():
    # TODO: flash a 'logged out' message here
    session.pop('username', None)
    return redirect(url_for('index'))


class AddExpApp(MethodView):
    
    form = AddExpAppForm
    
    def get_context(self, **kwargs):
        form = self.form(request.form)
        context = {'form': form}
        return context
    
    def get(self, **kwargs):
        context = self.get_context(**kwargs)
        if not g.logged_in:
            return redirect(url_for('login', return_to=request.base_url))
        
        return render_template('addexpapp.html', **context)
    
    def post(self, **kwargs):
        context = self.get_context(**kwargs)
        if not g.logged_in:
            return redirect(url_for('login', return_to=request.base_url))
        
        g.context = context
        form = context.get('form')
        
        if form.validate():
            ea = ExpApp(ea_id=form.ea_id.data,
                        description=form.description.data)
            ea.owners.append(g.user)
            ea.save()
            return redirect(url_for('user.index', username=g.username))

        return render_template('addexpapp.html', **context)


app.add_url_rule('/addexpapp', view_func=AddExpApp.as_view('addexpapp'))


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')
