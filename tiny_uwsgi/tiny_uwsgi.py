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
import pprint
try:
    import cProfile as profile
except:
    import profile


class FailSafe():

    def requestMainEntry(self, cookie, request, response):
        response.sendHeader()
        return 'OK'

ServiceDict = {
    'favicon.ico': {
        'obj': FailSafe(),
        'class': FailSafe,
    },
    'SYSTEM': {
        'profile': False,
        'profileobj': None,
    }
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
    if ServiceDict['SYSTEM']['profile'] is True:
        ServiceDict['SYSTEM']['profileobj'] = profile.Profile()
    for k, v in ServiceDict.iteritems():
        if k in ['favicon.ico', 'SYSTEM']:
            continue
        try:
            v['obj'] = v['class']()
        except:
            print traceback.format_exc()
            print 'service init fail', k
    pprint.pprint(ServiceDict)


class ServiceClassBase(object):

    def __init__(self):
        pass

    def getServiceDict(self):
        return ServiceDict

    def getServiceConfig(self):
        return ServiceDict[self.serviceName]

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
        if ServiceDict['SYSTEM']['profile'] is True:
            ServiceDict['SYSTEM']['profileobj'].enable()
        rtn = service['obj'].requestMainEntry(
            cookie, request, response)
    except:
        print traceback.format_exc()
        rtn = response.responseError('Bad Request', code=400)
    finally:
        if ServiceDict['SYSTEM']['profile'] is True:
            ServiceDict['SYSTEM']['profileobj'].disable()

    return rtn


def printProfileResult():
    if ServiceDict['SYSTEM']['profile'] is True:
        ServiceDict['SYSTEM']['profileobj'].print_stats()
    else:
        print 'No profile'


def registerService(serviceClass):
    def exposeToURL(oldfn):
        serviceClass.dispatchFnDict[oldfn.__name__] = oldfn
        setattr(serviceClass, oldfn.__name__, oldfn)
        return oldfn
    ServiceDict[serviceClass.serviceName] = {}
    ServiceDict[serviceClass.serviceName]['class'] = serviceClass
    return exposeToURL


def getRequestEntry(config):
    for k, v in config.iteritems():
        ServiceDict[k].update(config.get(k, {}))
    return uwsgiEntry
