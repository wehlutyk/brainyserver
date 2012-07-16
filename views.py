#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Views for the root of the app.

Methods:
  * ``before_request_mongodb``: store the mondodb object in g
  * ``before_request_loggedstatus``: store the LoggedStatus object in g

Classes:
  * ``FormMethodView``: provide default methods for a view using a form
  * ``Index``: welcome page for the website
  * ``Register``: let a user create an account
  * ``Login``: let a user log in
  * ``Logout``: log a user out
  * ``AddExpApp``: let a user add an Experiment App
  * ``About``: display the About page
  * ``Contact``: display the Contact page

"""


from abc import abstractproperty, abstractmethod

from flask import render_template, request, redirect, url_for, session, g
from flask.views import MethodView, MethodViewType

from brainyserver.forms import RegisterForm, LoginForm, AddExpAppForm
import brainyserver.mongodb as mongodb
from brainyserver.mongodb import Researcher, ExpApp
from brainyserver.loggedstatus import LoggedStatus, log_user_in, log_user_out


def before_request_mongodb():
    """Store the mondodb object in g."""
    g.mongodb = mongodb


def before_request_loggedstatus():
    """Store the LoggedStatus object in g."""
    username = session.get('username')
    g.loggedstatus = LoggedStatus(username)


class FormMethodView(MethodView):
    
    """Provide default methods for a view using a form.
    
    Abstract properties:
      * ``form``: the form class used in the view
      * ``template``: the template used to render the form
    
    Abstract methods:
      * ``check_applicable``: check that this page is applicable for the user
      * ``process_form``: process the form data
    
    Methods:
      * ``get_context``: get the form from the request, and store it in g
      * ``get``: answer a GET
      * ``post``: answer a POST
    
    """
    
    __metaclass__ = MethodViewType
    
    @abstractproperty
    def form(self):
        """Hold the form class that will be used."""
        raise NotImplementedError
    
    @abstractproperty
    def template(self):
        """Hold the template name to be rendered for the page."""
        raise NotImplementedError
    
    @abstractmethod
    def check_applicable(self):
        """Check that this page is applicable for the user."""
        raise NotImplementedError
    
    @abstractmethod
    def process_form(self):
        """Process the form data."""
        raise NotImplementedError
    
    def get_context(self):
        """Get the form from the request, and store it in g."""
        form = self.form(request.form)
        return_to = request.args.get('return_to')
        context_add = {'form': form, 'return_to': return_to}
        try:
            self.context.update(context_add)
        except AttributeError:
            self.context = context_add
        g.context = self.context
    
    def get(self):
        """Answer a GET."""
        ret = None
        
        self.get_context()
        ret = ret or self.check_applicable()
        ret = ret or render_template(self.template, **self.context)
        
        return ret
    
    def post(self):
        """Answer a POST."""
        ret = None
        
        self.get_context()
        ret = ret or self.check_applicable()
        ret = ret or self.process_form()
        ret = ret or render_template(self.template, **self.context)
        
        return ret


class Index(MethodView):
    
    """Welcome page for the website."""
    
    def get(self):
        """Answer a GET."""
        return render_template('base.html')


class Register(FormMethodView):
    
    """Let a user create an account."""
    
    form = RegisterForm
    template = 'register.html'
    
    def check_applicable(self):
        """Check that the user isn't already logged in."""
        if g.loggedstatus.logged_in:
            # TODO: flash an 'already logged in' message here
            return redirect(url_for('index'))
    
    def create_researcher(self, form):
        """Create the user in database."""
        r = Researcher(username=form.username.data, email=form.email.data)
        r.set_password(form.password.data)
        r.save()
        return r
    
    def process_form(self):
        """Read the form, create the user if valid, and log him in."""
        form = self.context.get('form')
        
        if form.validate():
            r = self.create_researcher(form)
            log_user_in(r)
            return redirect(url_for('user.index', username=r.username))


class Login(FormMethodView):
    
    """Let a user log in."""
    
    form = LoginForm
    template = 'login.html'
    
    def check_applicable(self):
        """Check that the user isn't already logged in."""
        if g.loggedstatus.logged_in:
            # TODO: flash an 'already logged in' message here
            return redirect(url_for('index'))
    
    def verify_credentials(self, form):
        """Verify provided credentials."""
        r = (Researcher.objects(username=form.username_email.data).first()
             or Researcher.objects(email=form.username_email.data).first())
        
        if not r:
            
            form.username_email.errors += ('Username or Email not found',)
            return False
        
        if not r.check_password(form.password.data):
            
            form.password.errors += ('Invalid password',)
            return False
        
        return r
    
    def process_form(self):
        """Verify provided credentials and log the user in if valid."""
        form = self.context.get('form')
        
        if form.validate():
            r = self.verify_credentials(form)
            
            if not r:
                return render_template('login.html', **self.context)
            
            log_user_in(r)
            redir_url = self.context.get('return_to',
                                url_for('user.index', username=r.username))
            return redirect(redir_url)


class Logout(MethodView):
    
    """Log a user out."""
    
    def get(self):
        log_user_out()
        return redirect(url_for('index'))


class AddExpApp(FormMethodView):
    
    """Let a user add an Experiment App."""
    
    form = AddExpAppForm
    template = 'addexpapp.html'
    
    def check_applicable(self):
        """Check that the user is logged in."""
        if not g.loggedstatus.logged_in:
            return redirect(url_for('login', return_to=request.base_url))
    
    def create_expapp(self, form):
        """Create the Experiment App in database."""
        ea = ExpApp(ea_name=form.ea_name.data,
                    description=form.description.data)
        ea.owners.append(g.user)
        ea.save()
    
    def process_form(self):
        """Create the Experiment App if the form is valid."""
        form = self.context.get('form')
        
        if form.validate():
            self.create_expapp(form)
            return redirect(url_for('user.index', username=g.username))


class About(MethodView):
    
    """Display the About page."""
    
    def get(self):
        """Answer a GET."""
        return render_template('about.html')


class Contact(MethodView):
    
    """Display the Contact page."""
    
    def get(self):
        """Answer a GET."""
        return render_template('contact.html')


def configure_frontend_app(app):
    app.before_request(before_request_mongodb)
    app.before_request(before_request_loggedstatus)
    
    app.add_url_rule('/', view_func=Index.as_view('index'))
    app.add_url_rule('/register', view_func=Register.as_view('register'))
    app.add_url_rule('/login', view_func=Login.as_view('login'))
    app.add_url_rule('/logout', view_func=Logout.as_view('logout'))
    app.add_url_rule('/addexpapp', view_func=AddExpApp.as_view('addexpapp'))
    app.add_url_rule('/about', view_func=About.as_view('about'))
    app.add_url_rule('/contact', view_func=Contact.as_view('contact'))
