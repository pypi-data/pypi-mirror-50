#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-App.
# @File         : App
# @Time         : 2019-08-08 10:26
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

import socket
from sanic import Sanic, response

from collections import OrderedDict
from traceback import format_exc  # https://www.cnblogs.com/klchang/p/4635040.html


# socket.SO_REUSEPORT = 15


class App(object):

    def __init__(self, debug=False, workers=1, version="0.0.1"):
        self.app = Sanic()
        self.debug = debug
        self.workers = workers
        self.version = version

        self.func = lambda x="test": x
        self.methods = None

    def run(self, host="0.0.0.0", port=8000):
        self.app.run(host, port, self.debug, worker=self.workers)

    def add_route(self, func, uri="/test", methods="GET"):
        self.func = func
        self.methods = methods

        self.app.add_route(self.handler, uri, frozenset({self.methods}))

    async def handler(self, request):
        """
        request.json: {'a': 1}
        request.args:  {'a': ['1']}
        """
        input = request.json if self.methods == 'POST' else request.args
        output = OrderedDict()

        if self.version:
            output['Version'] = self.version
        try:
            output['Score'] = self.func(**input)
        except Exception as error:
            output['Predict Error'] = error
            output['Predict Error Plus'] = format_exc().strip()
            output['Score'] = 0
        finally:
            if self.debug:
                output['Request Params'] = input

        return response.json(output)


if __name__ == '__main__':
    predict = lambda x=1, y=1: x + y
    app = App(debug=True)

    # app.app.add_route(app.handler, "/sum")
    # app.app.run()

    app.add_route(predict)
    app.run()
