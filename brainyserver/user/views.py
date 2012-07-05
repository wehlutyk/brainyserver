#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""User blueprint views."""


from flask import render_template, g, abort
from flask.views import MethodView

from brainyserver.user import user
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
    
    def get(self, **kwargs):
        return "TBD"


user.add_url_rule('/<ea_id>/edit/previz',
                  view_func=EditPreviz.as_view('editpreviz'))


@user.route('/<ea_id>/previz')
def previz_finalsource(**kwargs):
    return "TBD"
