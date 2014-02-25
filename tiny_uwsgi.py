#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""very thin python/uwsgi Framework
made by kasw
copyright 2013,2014
Version"""
Version = '3.0.0'

import Cookie as pyCookie
import urlparse
import pprint
import simplejson as json
import os
import sys
import traceback

from httpconst import HTTP_CODE, CONTENT_TYPE

# uwsgi specific
try:
    import uwsgi
    from uwsgidecorators import postfork
    srcdir = uwsgi.opt.get('ProgramBaseFolder', '.')
except:
    def postfork(f):
        print 'NOT uWSGI mode'
        return f
    # to use commonlib
    import os.path
    srcdir = os.path.dirname(os.path.abspath(sys.argv[0]))
    #sys.path.append(os.path.join(os.path.split(srcdir)[0], 'commonlib'))

ServiceDict = {
    'ServiceObjs': {},
    'serviceClasses': [],
}


class Request(object):

    def __init__(self, environ):
        self.environ = environ
        self.path = environ['PATH_INFO'].strip('/').split('/')
        self.args = urlparse.parse_qs(environ['QUERY_STRING'])
        self.logto = environ['wsgi.errors']
        self.json = {}

    def getPostFd(self):
        return self.environ['wsgi.input']

    def __str__(self):
        return "Request:{\nvars:%s,\npath:%s,\nargs:%s\n}" % (
            pprint.pformat(self.json),
            pprint.pformat(self.path),
            pprint.pformat(self.args),
        )

    def log(self, *args, **dargs):
        s = ''
        if args:
            s += pprint.pformat(args) + '\n'
        if dargs:
            s += pprint.pformat(dargs) + '\n'
        self.logto.write(s)

    def parseJsonPost(self):
        fd = self.getPostFd()
        postdata = fd.read()
        if postdata:
            self.json = json.loads(postdata)
        return self.json

    def parseFormPost(self):
        fd = self.getPostFd()
        postdata = fd.readline()
        if postdata:
            rtn = urlparse.parse_qs(postdata.decode(), True)
            for k, v in rtn.iteritems():
                self.json[k] = v[0]
        return self.json

    def parseGet(self):
        return self.args


class Response(object):

    def __init__(self, environ, start_response, cookie):
        self.headers = [None, ]
        # self.codestr = ''
        self.cookie = cookie
        self.start_response = start_response

        self.setContentType('.txt')
        self.setHTTPCode(200)

    def sendHeader(self):
        self.cookie.toHeader(self)
        self.start_response(self.codestr, self.headers)

    def setHTTPCode(self, c):
        self.codestr = '%d %s' % (c, HTTP_CODE[c])

    def addHeader(self, name, value):
        self.headers.append((name, value))

    def setRedirect(self, desturl):
        self.setHTTPCode(303)
        self.addHeader('Location', desturl)

    def setContentType(self, s):
        self.headers[0] = ('Content-type', CONTENT_TYPE[s])

    def __str__(self):
        return "Response:{\nheaders:%s,\ncodestr:%s\n}" % (
            pprint.pformat(self.headers),
            pprint.pformat(self.codestr),
        )

    def responseError(self, msg, code=404, msgtype='.txt'):
        self.setHTTPCode(code)
        self.setContentType(msgtype)
        self.sendHeader()
        return msg


class Cookie(object):

    def __init__(self, environ):
        self.cookie = pyCookie.SimpleCookie()
        if environ.get('HTTP_COOKIE'):
            self.cookie.load(environ.get('HTTP_COOKIE'))

    def toHeader(self, response):
        for k in self.cookie:
            response.headers.append((
                'Set-Cookie', self.cookie[k].OutputString()))

    def __str__(self):
        return """Cookie:%s""" % (
            pprint.pformat(self.cookie),
        )


class ServiceClassBase(object):

    def __init__(self):
        pass

    def getServiceDict(self):
        return ServiceDict

    def requestMainEntry(self, cookie, request, response):
        response.sendHeader()
        return 'OK'


@postfork
def ServiceInit():
    print sys.version
    print __doc__, Version
    print "server forked", uwsgi.worker_id()

    # additional init
    for ss in ServiceDict['serviceClasses']:
        ServiceDict['ServiceObjs'][ss.serviceName] = ss()
    print ServiceDict


def uwsgiEntry(environ, start_response):
    """ Main http request process
    """
    cookie = Cookie(environ)
    request = Request(environ)
    response = Response(environ, start_response, cookie)

    try:
        serviceobjs = ServiceDict['ServiceObjs']
        servicename = request.path[0]
        return serviceobjs[servicename].requestMainEntry(cookie, request, response)
    except:
        print traceback.format_exc()
        return response.responseError('Bad Request', code=400)


def registerService(serviceClass):
    def exposeToURL(oldfn):
        serviceClass.dispatchFnDict[oldfn.__name__] = oldfn
        setattr(serviceClass, oldfn.__name__, oldfn)
        # print 'register', serviceClass.__name__, oldfn.__name__
        return oldfn
    ServiceDict['serviceClasses'].append(serviceClass)
    return uwsgiEntry, exposeToURL