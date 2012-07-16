#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Manage the Brainyserver server."""


from flask.ext.script import Manager, Server
from brainyserver import create_app


manager = Manager(create_app)
manager.add_option('-m', '--mode', dest='mode', default='prod')


class RunMode(Server):
    
    def handle(self, app, *args, **kwargs):
        app.run(host=app.config['HOST'])


manager.add_command('runserver', RunMode())


if __name__ == '__main__':
    manager.run()
