import asyncio
import unittest
import os
from functools import wraps


def run_until_complete(fun):
    if not asyncio.iscoroutinefunction(fun):
        fun = asyncio.coroutine(fun)

    @wraps(fun)
    def wrapper(test, *args, **kw):
        loop = test.loop
        ret = loop.run_until_complete(fun(test, *args, **kw))
        return ret
    return wrapper

class BaseTest(unittest.TestCase):
    """Base test case for unittests.
    """

    def setUp(self):
        self.host = '127.0.0.1'
        self.port = 4150
        self.nsqlookupd_host = '127.0.0.1'
        self.nsqlookupd_port = 4161
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def tearDown(self):
        self.loop.close()
        del self.loop
