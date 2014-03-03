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
        # self.makeIndex(self.config['IndexDef'])

        self.makeTestData()

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

    def makeTestData(self):
        for i in range(10):
            self.db['userinfo'].insert(
                username='hello',
                email='hello@world.com',
                phone='0000',
                joindate=datetime.datetime.now()
            )


exposeToURL = registerService(Service1)

import datetime
import pprint


@exposeToURL
def dbInsert(self, args, kwdict):
    i = self.db['userinfo'].insert(
        username='hello',
        email='hello@world.com',
        phone='0000',
        joindate=datetime.datetime.now()
    )
    return str(i)


@exposeToURL
def dbSelect(self, args, kwdict):
    rows = self.db().select(self.db.userinfo.ALL, limitby=(0, 10))
    # return pprint.pformat(rows.as_dict())
    return str(len(rows))
