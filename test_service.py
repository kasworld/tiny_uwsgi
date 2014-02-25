#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""service main, service object
made by kasw
copyright 2014
Version"""
Version = '3.0.0'

import traceback


from tiny_uwsgi import ServiceClassBase, registerService


class TestService(ServiceClassBase):

    """ service class
    """
    dispatchFnDict = {}
    serviceName = 'TestService'

    def __init__(self):
        # print TestService.dispatchFnDict
        pass

    def requestMainEntry(self, cookie, request, response):
        try:
            request.parseJsonPost()
        except:
            print traceback.format_exc()
            return response.responseError('Bad Request', code=400)

        try:
            fnname = request.path[1]
            result = TestService.dispatchFnDict[
                fnname](request.args, request.json)
        except:
            print traceback.format_exc()
            return response.responseError('Bad Request', code=400)
        response.sendHeader()
        return result

application, exposeToURL = registerService(TestService)


@exposeToURL
def testFn(serviceObj, *args, **kwdict):
    # http://hostname/TestService/testFn
    return str(args) + str(kwdict)


if __name__ == "__main__":
    print TestService().testFn(5)


# vim:ts=4:sw=4:et
