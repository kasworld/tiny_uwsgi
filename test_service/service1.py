#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""tiny_uwsgi sample Service1
basic http service with db using web2py.dal
made by kasw
copyright 2014
Version"""
Version = '3.1.0'

import traceback
import datetime
import pprint
from tiny_uwsgi import ServiceBase, ProfileMixin, DispatcherMixin_AD
from dalobj import DBDataMixinBase


class Service1(ServiceBase, ProfileMixin, DispatcherMixin_AD, DBDataMixinBase):

    """ service class
    """
    dispatchFnDict = {}
    serviceName = 'Service1'

    def __init__(self):
        ServiceBase.__init__(self)
        ProfileMixin.__init__(self)
        DispatcherMixin_AD.__init__(self)

        self.config = self.getServiceConfig()

        DBDataMixinBase.__init__(
            self,
            self.config['dbconn']
        )
        self.loadAllTables(self.config['ObjDefs'])
        # self.makeIndex(self.config['IndexDef'])

        self.makeTestData()

    def makeTestData(self):
        for i in range(10):
            self.db['userinfo'].insert(
                username='hello',
                email='hello@world.com',
                phone='0000',
                joindate=datetime.datetime.now()
            )


Service1.registerService()


@Service1.exposeToURL
def dbInsert(self, args, kwdict):
    i = self.db['userinfo'].insert(
        username='hello',
        email='hello@world.com',
        phone='0000',
        joindate=datetime.datetime.now()
    )
    return str(i)


@Service1.exposeToURL
def dbSelect(self, args, kwdict):
    rows = self.db().select(self.db.userinfo.ALL, limitby=(0, 10))
    # return pprint.pformat(rows.as_dict())
    return str(len(rows))
