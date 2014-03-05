#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""very thin python/uwsgi Framework
made by kasw
copyright 2013,2014
Version"""
Version = '3.2.0'

import traceback
import sys
import signal
import pprint
try:
    import cProfile as profile
except:
    import profile


class FailSafe():
    profile = False

    def requestMainEntry(self, cookie, request, response):
        response.sendHeader()
        return 'OK'

ServiceDict = {
    'favicon.ico': {
        'obj': FailSafe(),
        'class': FailSafe,
    },
    'SYSTEM': {
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
    for k, v in ServiceDict.iteritems():
        if k in ['favicon.ico', 'SYSTEM']:
            continue
        try:
            v['obj'] = v['class']()
        except:
            print traceback.format_exc()
            print 'service init fail', k
    # pprint.pprint(ServiceDict)


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
        if getattr(service['obj'], 'profile', False) is True:
            service['obj'].profileobj.enable()
        rtn = service['obj'].requestMainEntry(
            cookie, request, response)
    except:
        print traceback.format_exc()
        rtn = response.responseError('Bad Request', code=400)
    finally:
        if getattr(service['obj'], 'profile', False) is True:
            service['obj'].profileobj.disable()
    return rtn


def getRequestEntry(config):
    for k, v in config.iteritems():
        if k in ServiceDict:
            ServiceDict[k].update(config.get(k, {}))
        else:
            print '[Warning] not inited service in config', k
    return uwsgiEntry


# ===========

class ServiceBase(object):

    def getServiceDict(self):
        return ServiceDict

    def getServiceConfig(self):
        return ServiceDict[self.serviceName]

    @classmethod
    def registerService(serviceClass):
        if serviceClass.serviceName in ServiceDict:
            print '[Warning] already registered service name', serviceClass.serviceName
        else:
            ServiceDict[serviceClass.serviceName] = {'class': serviceClass}


class ProfileMixin(object):

    def __init__(self):
        self.profile = self.getServiceConfig().get('profile', False)
        if self.profile is True:
            self.profileobj = profile.Profile()

    def printProfileResult(self):
        if self.profile is True:
            self.profileobj.print_stats()
        else:
            print 'No profile'


class DispatcherMixin_CRR(object):

    def requestMainEntry(self, cookie, request, response):
        try:
            request.parseJsonPost()
        except:
            print traceback.format_exc()
            return response.responseError('Bad Request', code=400)

        try:
            fnname = request.path[1]
            result = self.dispatchFnDict[
                fnname](self, cookie, request, response)
        except:
            print traceback.format_exc()
            return response.responseError('Bad Request', code=400)
        response.sendHeader()
        return result

    @classmethod
    def exposeToURL(serviceClass, oldfn):
        serviceClass.dispatchFnDict[oldfn.__name__] = oldfn
        setattr(serviceClass, oldfn.__name__, oldfn)
        return oldfn


class DispatcherMixin_AD(object):

    def requestMainEntry(self, cookie, request, response):
        try:
            request.parseJsonPost()
        except:
            print traceback.format_exc()
            return response.responseError('Bad Request', code=400)

        try:
            fnname = request.path[1]
            result = self.dispatchFnDict[
                fnname](self, request.args, request.json)
        except:
            print traceback.format_exc()
            return response.responseError('Bad Request', code=400)
        response.sendHeader()
        return result

    @classmethod
    def exposeToURL(serviceClass, oldfn):
        serviceClass.dispatchFnDict[oldfn.__name__] = oldfn
        setattr(serviceClass, oldfn.__name__, oldfn)
        return oldfn

'''
class Service0(ServiceBase, ProfileMixin, DispatcherMixin):

    """ basic service class
    """
    serviceName = 'Service0'
    dispatchFnDict = {}

Service0.registerService()


@Service0.exposeToURL
def info(self, cookie, request, response):
    return 'service0' + str(Service0.exposeToURL)


class Service1(ServiceBase, ProfileMixin, DispatcherMixin):

    """ basic service class
    """
    serviceName = 'Service1'
    dispatchFnDict = {}

Service1.registerService()


@Service1.exposeToURL
def info2(self, cookie, request, response):
    return 'service1' + self.serviceName


config = dict(
    Service0=dict(
        profile=True
    ),
    Service1=dict(
        profile=True
    ),
)
application = getRequestEntry(config)
'''
