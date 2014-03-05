#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""tiny_uwsgi sample Service0
basic server
made by kasw
copyright 2014
Version"""
Version = '3.1.0'

import os
import signal
import pprint
import uwsgi

from tiny_uwsgi import ServiceBase, DispatcherMixin_CRR


class Service0(ServiceBase, DispatcherMixin_CRR):

    """ basic service class
    """
    serviceName = 'Service0'
    dispatchFnDict = {}


Service0.registerService()


@Service0.exposeToURL
def uwsgiInfo(self, cookie, request, response):
    return pprint.pformat(uwsgi.__dict__)


@Service0.exposeToURL
def envInfo(self, cookie, request, response):
    return pprint.pformat(request.environ)


@Service0.exposeToURL
def reqInfo(self, cookie, request, response):
    return str(request)


@Service0.exposeToURL
def sysInfo(self, cookie, request, response):
    return pprint.pformat(self.getServiceDict())


@Service0.exposeToURL
def stat(self, cookie, request, response):
    os.kill(uwsgi.masterpid(), signal.SIGUSR1)
    return 'ok'


@Service0.exposeToURL
def testFn(self, cookie, request, response):
    args, kwdict = request.args, request.json
    return str(self.serviceName) + str(args) + str(kwdict)
