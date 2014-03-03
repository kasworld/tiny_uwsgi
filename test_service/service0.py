#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""tiny_uwsgi sample Service0
basic server
made by kasw
copyright 2014
Version"""
Version = '3.0.0'

import traceback

from tiny_uwsgi import ServiceClassBase, registerService


class Service0(ServiceClassBase):

    """ service class
    """
    dispatchFnDict = {}
    serviceName = 'Service0'

    def __init__(self):
        ServiceClassBase.__init__(self)

    def requestMainEntry(self, cookie, request, response):
        try:
            request.parseJsonPost()
        except:
            print traceback.format_exc()
            return response.responseError('Bad Request', code=400)

        try:
            fnname = request.path[1]
            result = Service0.dispatchFnDict[
                fnname](self, cookie, request, response)
        except:
            print traceback.format_exc()
            return response.responseError('Bad Request', code=400)
        response.sendHeader()
        return result

exposeToURL = registerService(Service0)


import pprint
import uwsgi


@exposeToURL
def uwsgiInfo(self, cookie, request, response):
    return pprint.pformat(uwsgi.__dict__)


@exposeToURL
def envInfo(self, cookie, request, response):
    return pprint.pformat(request.environ)


@exposeToURL
def reqInfo(self, cookie, request, response):
    return str(request)


@exposeToURL
def testFn(self, cookie, request, response):
    # http://hostname/Service0/testFn
    args, kwdict = request.args, request.json
    return str(self.serviceName) + str(args) + str(kwdict)
