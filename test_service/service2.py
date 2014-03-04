#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""tiny_uwsgi sample Service2
advanced uwsgi use , async, gevent

check if
gevent 1.0.0 or more install
install locally
pip install --user gevent

made by kasw
copyright 2014
Version"""
Version = '3.0.0'

import gevent
if gevent.version_info < (1, 0, 0):
    print 'gevent 1.0.0 or more need', gevent.version_info

import uwsgi
import uwsgidecorators

import traceback
import signal
import os
from tiny_uwsgi import ServiceClassBase, registerService


def microtask(wid):
    print "i am a gevent task"
    gevent.sleep(10)
    print "10 seconds elapsed in worker id %d" % wid


class Service2(ServiceClassBase):

    """ service class
    """
    dispatchFnDict = {}
    serviceName = 'Service2'

    def __init__(self):
        ServiceClassBase.__init__(self)
        if not uwsgi.cache_exists('Service2Counter'):
            uwsgi.cache_set('Service2Counter', '0')
        if not uwsgi.cache_exists('Service2Timer'):
            uwsgi.cache_set('Service2Timer', '0')
        print uwsgi.queue_size
        gevent.spawn(microtask, uwsgi.worker_id())
        print 'after gevent.spawn'

    def requestMainEntry(self, cookie, request, response):
        try:
            request.parseJsonPost()
        except:
            print traceback.format_exc()
            return response.responseError('Bad Request', code=400)

        try:
            fnname = request.path[1]
            result = Service2.dispatchFnDict[
                fnname](self, cookie, request, response)
        except:
            print traceback.format_exc()
            return response.responseError('Bad Request', code=400)
        response.sendHeader()
        return result


@uwsgidecorators.timer(1)
def hello_timer(num):
    i = int(uwsgi.cache_get('Service2Timer'))
    i += 1
    uwsgi.cache_update('Service2Timer', str(i))


exposeToURL = registerService(Service2)


import datetime


@exposeToURL
def counter(self, cookie, request, response):
    i = int(uwsgi.cache_get('Service2Counter'))
    i += 1
    uwsgi.cache_update('Service2Counter', str(i))
    return "{0} {1}".format(i, uwsgi.cache_get('Service2Timer'))


@exposeToURL
def clock(self, cookie, request, response):
    #response.addHeader('refresh', '1')
    return datetime.datetime.now().isoformat()


@exposeToURL
def stat(self, cookie, request, response):
    # uwsgi.signal(signal.SIGUSR1)
    os.kill(uwsgi.masterpid(), signal.SIGUSR1)
    # uwsgi.masterpid()
    return 'ok'


# @exposeToURL
# def profile(self, cookie, request, response):
#     # uwsgi.signal(signal.SIGUSR1)
#     os.kill(uwsgi.masterpid(), 98)
#     # uwsgi.masterpid()
#     return 'ok'
