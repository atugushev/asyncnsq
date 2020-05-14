import asyncio
from ._testutils import run_until_complete, BaseTest
from asyncnsq.tcp.reader import create_reader
from asyncnsq.tcp.writer import create_writer
from asyncnsq.http import NsqdHttpWriter


class NsqTest(BaseTest):

    def setUp(self):
        self.topic = b'foo'
        super().setUp()

    def tearDown(self):
        conn = NsqdHttpWriter(self.host, self.port+1, loop=self.loop)
        try:
            self.loop.run_until_complete(conn.delete_topic(self.topic))
        except Exception:
            # TODO: fix
            pass
        super().tearDown()

    # @run_until_complete
    # def test_basic_instance(self):
    #     nsq = yield from create_nsq(host=self.host, port=self.port,
    #                                 heartbeat_interval=30000,
    #                                 feature_negotiation=True,
    #                                 tls_v1=True,
    #                                 snappy=False,
    #                                 deflate=False,
    #                                 deflate_level=0,
    #                                 loop=self.loop)
    #     yield from nsq.pub(b'foo', b'bar')
    #     yield from nsq.pub(b'foo', b'bar')
    #     yield from nsq.pub(b'foo', b'bar')
    #     yield from nsq.pub(b'foo', b'bar')
    #     yield from nsq.pub(b'foo', b'bar')
    #
    #     yield from nsq.sub(b'foo', b'bar')
    #     for i, waiter in enumerate(nsq.wait_messages()):
    #         # import ipdb; ipdb.set_trace()
    #         if i == 0:
    #             yield from nsq.rdy(3)
    #             # yield from nsq.rdy(1)
    #         message = yield from waiter
    #         yield from message.fin()
    #         break


    @run_until_complete
    def test_consumer(self):
        nsq = yield from create_writer(host=self.host, port=self.port,
                                       heartbeat_interval=30000,
                                       feature_negotiation=True,
                                       tls_v1=True,
                                       snappy=False,
                                       deflate=False,
                                       deflate_level=0,
                                       loop=self.loop)
        for i in range(100):
            yield from nsq.pub(b'foo', f'xxx:{i}'.encode())

        yield from asyncio.sleep(0.1, loop=self.loop)
        reader = yield from create_reader(nsqd_tcp_addresses=[f'{self.host}:{self.port}'],
                               max_in_flight=30, loop=self.loop)
        yield from reader.subscribe(b'foo', b'bar')

        msgs = []
        for i, waiter in enumerate(reader.wait_messages()):

            # yield from msg.fin()
            print('-----msgs', len(msgs))

            if reader.is_starved():
                print(">>>>>>>>msgs in list: {}".format(len((msgs))))
                for m in msgs:
                    yield from m.fin()
                msgs = []

            msg = yield from waiter
            msgs.append(msg)

            if i == 99:
                break

        # TODO must be something asserted
