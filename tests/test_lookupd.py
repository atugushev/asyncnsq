from ._testutils import run_until_complete, BaseTest
from asyncnsq.http import NsqLookupd


class NsqLookupdTest(BaseTest):
    """
    :see: http://nsq.io/components/nsqd.html
    """

    @run_until_complete
    def test_ok(self):
        conn = NsqLookupd(self.nsqlookupd_host, self.nsqlookupd_port, loop=self.loop)
        res = yield from conn.ping()
        self.assertEqual(res, 'OK')

    @run_until_complete
    def test_info(self):
        conn = NsqLookupd(self.nsqlookupd_host, self.nsqlookupd_port, loop=self.loop)
        res = yield from conn.info()
        self.assertTrue('version' in res)

    @run_until_complete
    def test_lookup(self):
        conn = NsqLookupd(self.nsqlookupd_host, self.nsqlookupd_port, loop=self.loop)
        res = yield from conn.lookup('foo')
        self.assertIn('producers', res)

    @run_until_complete
    def test_topics(self):
        conn = NsqLookupd(self.nsqlookupd_host, self.nsqlookupd_port, loop=self.loop)
        res = yield from conn.topics()
        self.assertIn('topics', res)

    @run_until_complete
    def test_channels(self):
        conn = NsqLookupd(self.nsqlookupd_host, self.nsqlookupd_port, loop=self.loop)
        res = yield from conn.channels('foo')
        self.assertIn('channels', res)

    @run_until_complete
    def test_nodes(self):
        conn = NsqLookupd(self.nsqlookupd_host, self.nsqlookupd_port, loop=self.loop)
        res = yield from conn.nodes()
        self.assertIn('producers', res)
