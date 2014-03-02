#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""tiny_uwsgi sample Service2
made by kasw
copyright 2014
Version"""
Version = '3.0.0'

import uwsgi
import traceback
import pprint
from tiny_uwsgi import ServiceClassBase, registerService


class Service2(ServiceClassBase):

    """ service class
    """
    dispatchFnDict = {}
    serviceName = 'Service2'

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
            result = Service2.dispatchFnDict[
                fnname](self, cookie, request, response)
        except:
            print traceback.format_exc()
            return response.responseError('Bad Request', code=400)
        response.sendHeader()
        return result

exposeToURL = registerService(Service2)


@exposeToURL
def testFn(self, cookie, request, response):
    return pprint.pformat(uwsgi.__dict__)

import datetime


@exposeToURL
def clock(self, cookie, request, response):
    #response.addHeader('refresh', '1')
    return datetime.datetime.now().isoformat()
