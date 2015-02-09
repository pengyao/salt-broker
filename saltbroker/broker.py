# -*- coding: utf-8 -*-
'''
A lightweight proxy for saltstack
'''

# Import python libs
import logging
import multiprocessing

# Import third party libs
import zmq

# Import salt libs
import salt.minion
import salt.utils

# Import saltbroker utils
from saltbroker.utils import appendproctitle

log = logging.getLogger(__name__)

class PubBroker(multiprocessing.Process):
    '''
    Publish broker, a simple zeromq PUB/SUB proxy
    '''
    def __init__(self, opts):
        super(PubBroker, self).__init__()
        self.opts = opts
        self.opts['master_ip'] = salt.utils.dns_check(self.opts['master'])

    def run(self):
        '''
        Build a PUB/SUB proxy

        http://zguide.zeromq.org/py:wuproxy
        '''
        appendproctitle(self.__class__.__name__)
        context = zmq.Context()

        # Set up a master SUB sock
        master_pub = 'tcp://{0}:{1}'.format(self.opts['master_ip'],
                                            self.opts['publish_port'])
        sub_sock = context.socket(zmq.SUB)
        log.info('Starting set up a broker SUB sock on {0}'.format(master_pub))
        sub_sock.connect(master_pub)

        # Set up a broker PUB sock
        pub_uri = 'tcp://{0}:{1}'.format(self.opts['interface'],
                                         self.opts['publish_port'])
        pub_sock = context.socket(zmq.PUB)
        log.info('Starting set up a broker PUB sock on {0}'.format(pub_uri))
        pub_sock.bind(pub_uri)

        # Subscribe everything from master
        sub_sock.setsockopt(zmq.SUBSCRIBE, b'')

        try:
            # Send  messages to broker PUB sock
            while True:
                message = sub_sock.recv_multipart()
                pub_sock.send_multipart(message)
        except KeyboardInterrupt:
            log.warn('Stopping the PubBorker')
            if sub_sock.closed is False:
                sub_sock.setsockopt(zmq.LINGER, 1)
                sub_sock.close()
            if pub_sock.closed is False:
                pub_sock.setsockopt(zmq.LINGER, 1)
                pub_sock.close()
            if context.closed is False:
                context.term()


class RetBroker(multiprocessing.Process):
    '''
    Ret broker, a simple zeromq message queuing broker
    '''
    def __init__(self, opts):
        super(RetBroker, self).__init__()
        self.opts = opts
        self.opts['master_ip'] = salt.utils.dns_check(self.opts['master'])

    def run(self):
        '''
        Build a QUEUE device

        http://zguide.zeromq.org/py:msgqueue
        '''
        appendproctitle(self.__class__.__name__)
        context = zmq.Context()

        # Set up a router sock to receive results from minions
        router_uri = 'tcp://{0}:{1}'.format(self.opts['interface'],
                                            self.opts['ret_port'])
        router_sock = context.socket(zmq.ROUTER)
        log.info(
            'Starting set up a broker ROUTER sock on {0}'.format(router_uri))
        router_sock.bind(router_uri)

        # Set up a dealer sock to send results to master ret interface
        dealer_sock = context.socket(zmq.DEALER)
        self.opts['master_uri'] = 'tcp://{0}:{1}'.format(self.opts['master_ip'],
                                                      self.opts['ret_port'])
        log.info(
            'Starting set up a broker DEALER sock on {0}'.format(
                self.opts['master_uri']))
        dealer_sock.connect(self.opts['master_uri'])

        try:
            # Forward all results
            zmq.device(zmq.QUEUE, router_sock, dealer_sock)
        except KeyboardInterrupt:
            log.warn('Stopping the RetBroker')
            if router_sock.closed is False:
                router_sock.setsockopt(zmq.LINGER, 1)
                router_sock.close()
            if dealer_sock.closed is False:
                dealer_sock.setsockopt(zmq.LINGER, 1)
                dealer_sock.close()
            if context.closed is False:
                context.term()



class Broker(object):
    '''
    Salt broker
    '''
    def __init__(self, opts):
        '''
        Create a salt broker instance
        '''
        self.opts = opts

    def start(self):
        '''
        Turn on broker components
        '''
        log.info(
            'salt-broker is starting as user {0!r}'.format(
                salt.utils.get_user())
        )
        log.info('starting pub broker......')
        self.pub_broker = PubBroker(self.opts)
        self.pub_broker.start()
        log.info('starting ret broker......')
        self.ret_broker = RetBroker(self.opts)
        self.ret_broker.start()

