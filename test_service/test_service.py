#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""tiny_uwsgi sample server main
made by kasw
copyright 2014
Version"""
Version = '3.0.0'

from tiny_uwsgi import getRequestEntry
import service0
import service1
import service2

config = dict(
    Service1=dict(
        dbconn=dict(
            uri="sqlite:memory",
        ),

        ObjDefs=(
            ('userinfo',
             ('username', 'string', dict(length=255, notnull=True)),
             ('email', 'string', dict(length=255, notnull=True)),
             ('phone', 'string', dict(length=255, notnull=True)),
             ('joindate', 'datetime', dict(notnull=True))
             ),
        ),
        IndexDef={
            'userinfo': ('username', 'email'),
        }

    ),
)

application = getRequestEntry(config)

if __name__ == "__main__":
    print service0.Service0.serviceName
    print service1.Service1.serviceName
    print service2.Service2.serviceName
