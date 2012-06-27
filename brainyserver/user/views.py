#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""User blueprint views."""


from flask import render_template, request, g, redirect, url_for, abort
from flask.views import MethodView

from brainyserver.user import user
from brainyserver.user.forms import AddExpAppForm
from brainyserver.mongodb import ExpApp, Researcher


class Index(MethodView):
    
    def get_context(self, **kwargs):
        username = kwargs['username']
        user = Researcher.objects(username=username).first()
        context = {'username': username, 'user': user}
        return context
    
    def get(self, **kwargs):
        """User home page."""
        context = self.get_context(**kwargs)
        g.context = context
        username = context['username']
        
        if Researcher.objects(username=username).count() == 0:
            abort(404)
        
        return render_template('index.html')


user.add_url_rule('/', view_func=Index.as_view('index'))


class AddExpApp(MethodView):
    
    form = AddExpAppForm
    
    def get_context(self, **kwargs):
        username = kwargs['username']
        form = self.form(request.form)
        user = Researcher.objects(username=username).first()
        context = {'form': form, 'username': username, 'user': user}
        return context
    
    def get(self, **kwargs):
        context = self.get_context()
        return render_template('addexpapp.html', **context)
    
    def post(self, **kwargs):
        context = self.get_context(kwargs)
        g.context = context
        form = context.get('form')
        
        if form.validate():
            ea = ExpApp(ea_id=form.ea_id.data,
                        description=form.description.data)
            ea.owners.append(g.user)
            ea.save()
            return redirect(url_for('.index', username=g.username))

        return render_template('addexpapp.html', **context)


user.add_url_rule('/addexpapp', view_func=AddExpApp.as_view('addexpapp'))
