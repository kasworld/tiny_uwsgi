#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""tiny_uwsgi sample spool test
advanced uwsgi use , spool

check if
gevent 1.0.0 or more install
install locally
pip install --user gevent

made by kasw
copyright 2014
Version"""
Version = '3.1.0'

import gevent
if gevent.version_info < (1, 0, 0):
    print 'gevent 1.0.0 or more need', gevent.version_info

import uwsgidecorators


@uwsgidecorators.spoolforever
def runAlways(args):
    gevent.sleep(0)

#runAlways.spool(dict(hello='world'))


@uwsgidecorators.spool
def testSpool(args):
    pass
