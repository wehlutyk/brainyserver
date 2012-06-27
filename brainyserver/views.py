#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Views for the root of the app."""


from flask import render_template, request, redirect, url_for
from flask.views import MethodView

from brainyserver import app
from brainyserver.crypto import encrypt_password
from brainyserver.forms import RegisterForm
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
            r = Researcher()
            r.username = form.username.data
            r.email = form.email.data
            pwsalt, pwhash = encrypt_password(form.email.data)
            r.pwsalt = pwsalt
            r.pwhash = pwhash
            r.save()
            
            return redirect(url_for('index'))

        return render_template('register.html', **context)


app.add_url_rule('/register', view_func=Register.as_view('register'))


#class Login(MethodView):
#    
#    form = model_form(Researcher)
#    
#    def get_context(self):
#        form = self.form(request.form)
#
#        context = {'form': form}
#        return context
#    
#    def get(self):
#        context = self.get_context()
#        return render_template('register.html', **context)
#    
#    def post(self):
#        context = self.get_context()
#        form = context.get('form')
#        
#        if form.validate():
#            researcher = Researcher()
#            form.populate_obj(researcher)
#            researcher.save()
#            
#            return redirect(url_for('index'))
#
#        return render_template('register.html', **context)

