from ._testutils import run_until_complete, BaseTest
from asyncnsq.tcp.writer import create_writer


class NsqTCPProducerTest(BaseTest):

    @run_until_complete
    def test_publish(self):
        nsq_producer = yield from create_writer(host=self.host, port=self.port,
                                                tls_v1=False,
                                                loop=self.loop)
        ok = yield from nsq_producer.pub(b'baz', b'producer msg')
        self.assertEqual(ok, b'OK')

    @run_until_complete
    def test_mpublish(self):
        nsq_producer = yield from create_writer(host=self.host, port=self.port,
                                                tls_v1=False,
                                                loop=self.loop)
        messages = ['baz:1', b'baz:2', 3.14, 42]
        ok = yield from nsq_producer.mpub('baz', *messages)
        self.assertEqual(ok, b'OK')
