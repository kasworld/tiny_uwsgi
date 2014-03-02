#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""tiny_uwsgi sample Service1
basic http service with db using web2py.dal
made by kasw
copyright 2014
Version"""
Version = '3.0.0'

import traceback
from tiny_uwsgi import ServiceClassBase, DBDataMixinBase, registerService


class Service1(ServiceClassBase, DBDataMixinBase):

    """ service class
    """
    dispatchFnDict = {}
    serviceName = 'Service1'

    def __init__(self):
        ServiceClassBase.__init__(self)
        self.config = self.getServiceConfig()

        DBDataMixinBase.__init__(
            self,
            self.config['dbconn']
        )
        self.loadAllTables(self.config['ObjDefs'])
        #self.makeIndex(self.config['IndexDef'])

    def requestMainEntry(self, cookie, request, response):
        try:
            request.parseJsonPost()
        except:
            print traceback.format_exc()
            return response.responseError('Bad Request', code=400)

        try:
            fnname = request.path[1]
            result = Service1.dispatchFnDict[
                fnname](self, request.args, request.json)
        except:
            print traceback.format_exc()
            return response.responseError('Bad Request', code=400)
        response.sendHeader()
        return result

exposeToURL = registerService(Service1)


@exposeToURL
def testFn(self, args, kwdict):
    # http://hostname/Service1/testFn
    return str(self.serviceName) + str(args) + str(kwdict)
