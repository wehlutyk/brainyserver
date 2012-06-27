#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Manage the Brainyserver server."""


from flask.ext.script import Manager, Server
from brainyserver import app


manager = Manager(app)

# Turn on debugger by default and reloader.

manager.add_command('runserver', Server(use_debugger = True,
                                        use_reloader = True,
                                        host = '0.0.0.0'))


if __name__ == '__main__':
    manager.run()
