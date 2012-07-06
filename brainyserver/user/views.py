#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""User blueprint views."""


import json

from flask import render_template, g, abort, request, redirect, url_for
from flask.views import MethodView

from brainyserver.user import user
from brainyserver.user.forms import EditPrevizForm
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
        
        return render_template('user/index.html')


user.add_url_rule('/', view_func=Index.as_view('index'))


class ExploreExpApp(MethodView):
    
    def get_context(self, **kwargs):
        username = kwargs['username']
        user = Researcher.objects(username=username).first()
        ea_id = kwargs['ea_id']
        ea = ExpApp.objects(ea_id=ea_id).first()
        context = {'username': username, 'user': user, 'ea_id': ea_id,
                   'ea': ea}
        return context
    
    def get(self, **kwargs):
        context = self.get_context(**kwargs)
        if context['ea'] is None:
            abort(404)
        
        if (context['username'] != g.username or
            g.user not in context['ea'].owners):
            abort(403)
        
        g.context = context
        return render_template('user/exploreexpapp.html')


user.add_url_rule('/<ea_id>',
                  view_func=ExploreExpApp.as_view('exploreexpapp'))


class EditPreviz(MethodView):
    
    form = EditPrevizForm
    
    def get_context(self, **kwargs):
        username = kwargs['username']
        user = Researcher.objects(username=username).first()
        ea_id = kwargs['ea_id']
        ea = ExpApp.objects(ea_id=ea_id).first()
        form = self.form(request.form)
        fdata = form.source.data
        form.source.data = fdata if fdata else ea.previzpjs
        context = {'form': form, 'username': username, 'user': user,
                   'ea_id': ea_id, 'ea': ea}
        return context
    
    def get(self, **kwargs):
        context = self.get_context(**kwargs)
        if context['ea'] is None:
            abort(404)
        
        if (context['username'] != g.username or
            g.user not in context['ea'].owners):
            abort(403)
        
        g.context = context
        return render_template('user/editpreviz.html', **context)
    
    def post(self, **kwargs):
        context = self.get_context(**kwargs)
        if context['ea'] is None:
            abort(404)
        
        if (context['username'] != g.username or
            g.user not in context['ea'].owners):
            abort(403)
        
        g.context = context
        form = context.get('form')
        
        if form.validate():
            context['ea'].previzpjs = form.source.data
            context['ea'].save()
            return redirect(url_for('.exploreexpapp', ea_id=context['ea_id'],
                                    username=g.username))

        return render_template('user/editpreviz.html', **context)



user.add_url_rule('/<ea_id>/edit/previz',
                  view_func=EditPreviz.as_view('editpreviz'))


class PrevizPjs(MethodView):
    
    def get_context(self, **kwargs):
        username = kwargs['username']
        user = Researcher.objects(username=username).first()
        ea_id = kwargs['ea_id']
        ea = ExpApp.objects(ea_id=ea_id).first()
        context = {'username': username, 'user': user, 'ea_id': ea_id,
                   'ea': ea}
        return context
    
    def get(self, **kwargs):
        context = self.get_context(**kwargs)
        if context['ea'] is None:
            abort(404)
        
        if (context['username'] != g.username or
            g.user not in context['ea'].owners):
            abort(403)
        
        previzpjs = context['ea'].previzpjs
        return previzpjs if previzpjs else '// No previz found'


user.add_url_rule('/<ea_id>/previz.pjs',
                  view_func=PrevizPjs.as_view('previzpjs'))


def dl_to_ld(dl):
    """Convert a list of dicts to a dict of lists of values inside the
    dicts."""
    keys = set([])
    for d in dl:
        keys.update(d.keys())
    
    ld = dict((k, []) for k in keys)
    for d in dl:
        for k in keys:
            ld[k].append(d.get(k))
    
    return ld

class Data(MethodView):
    
    def get_context(self, **kwargs):
        username = kwargs['username']
        user = Researcher.objects(username=username).first()
        ea_id = kwargs['ea_id']
        ea = ExpApp.objects(ea_id=ea_id).first()
        context = {'username': username, 'user': user, 'ea_id': ea_id,
                   'ea': ea}
        return context
    
    def get(self, **kwargs):
        context = self.get_context(**kwargs)
        if context['ea'] is None:
            abort(404)
        
        if (context['username'] != g.username or
            g.user not in context['ea'].owners):
            abort(403)
        
        data = dl_to_ld([r.data for r in context['ea'].results])
        return json.dumps(data)


user.add_url_rule('/<ea_id>/data',
                  view_func=Data.as_view('data'))
