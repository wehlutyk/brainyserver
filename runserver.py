#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Run the Brainyserver server."""


from brainyserver import app


if __name__ == '__main__':
    app.run(host='0.0.0.0')
