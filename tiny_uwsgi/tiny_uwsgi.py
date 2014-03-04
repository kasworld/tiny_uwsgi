#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""very thin python/uwsgi Framework
made by kasw
copyright 2013,2014
Version"""
Version = '3.0.0'

import traceback
import sys
import signal
try:
    import cProfile as profile
except:
    import profile

ServiceDict = {
}

# uwsgi specific
import uwsgi
import uwsgidecorators

from tiny_crr import Cookie, Request, Response


@uwsgidecorators.postfork
def ServiceInit():
    print sys.version
    print __doc__, Version
    print "server forked ", uwsgi.worker_id()

    # additional init
    print ServiceDict
    for k, v in ServiceDict.iteritems():
        try:
            v['obj'] = v['class']()
            if v['config']['profile'] is True:
                v['profileobj'] = profile.Profile()
        except:
            print traceback.format_exc()
            print 'service init fail', k

    print ServiceDict


class ServiceClassBase(object):

    def __init__(self):
        pass

    def getServiceDict(self):
        return ServiceDict

    def getServiceConfig(self):
        return ServiceDict[self.serviceName]['config']

    def requestMainEntry(self, cookie, request, response):
        response.sendHeader()
        return 'OK'


def uwsgiEntry(environ, start_response):
    """ Main http request process
    """
    cookie = Cookie(environ)
    request = Request(environ)
    response = Response(environ, start_response, cookie)

    try:
        servicename = request.path[0]
        service = ServiceDict[servicename]
    except:
        print traceback.format_exc()
        rtn = response.responseError('Bad Request', code=400)
        return rtn

    try:
        if service['config']['profile'] is True:
            service['profileobj'].enable()
        rtn = service['obj'].requestMainEntry(
            cookie, request, response)
    except:
        print traceback.format_exc()
        rtn = response.responseError('Bad Request', code=400)
    finally:
        if service['config']['profile'] is True:
            service['profileobj'].disable()

    return rtn


#@uwsgidecorators.signal(98)
def printProfileResult(num):
    for k, v in ServiceDict.iteritems():
        if v['config']['profile'] is True:
            v['profileobj'].print_stats()
        else:
            return 'No profile'


def registerService(serviceClass):
    print serviceClass.serviceName

    def exposeToURL(oldfn):
        serviceClass.dispatchFnDict[oldfn.__name__] = oldfn
        setattr(serviceClass, oldfn.__name__, oldfn)
        # print 'register', serviceClass.__name__, oldfn.__name__
        return oldfn
    ServiceDict[serviceClass.serviceName] = {}
    ServiceDict[serviceClass.serviceName]['class'] = serviceClass
    return exposeToURL


def getRequestEntry(config):
    for k, v in ServiceDict.iteritems():
        ServiceDict[k]['config'] = config.get(k, {'profile': False})
    return uwsgiEntry
