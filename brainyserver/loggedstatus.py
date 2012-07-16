#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Manage logged status.

Methods:
  * ``log_user_in``: log a user in
  * ``log_user_out``: log a user out

Classes:
  * ``LoggedStatus``: store the logged in status of a request

"""

from flask import session

from brainyserver.mongodb import Researcher


def log_user_in(user):
    """Log a user in."""
    session['username'] = user.username


def log_user_out():
    """Log a user out."""
    session.pop('username', None)


class LoggedStatus(object):
    
    """Store the logged in status of a request.
    
    Instance attributes:
      * ``logged_in``: True if a user is logged in, False otherwise
      * ``user``: the mongodb.Researcher object representing the logged in
        user; None if no user is logged in
      * ``username``: the username of the user logged in; None if no user is
        logged in
    
    """
    
    def __init__(self, username):
        if username:
            
            self.logged_in = True
            self.user = Researcher.objects(username=username).first()
            self.username = username
        
        else:
            
            self.logged_in = False
            self.user = None
            self.username = None

