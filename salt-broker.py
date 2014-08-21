#!/usr/bin/env python

import zmq
import multiprocessing

class Broker():
    def __init__(self, master, ret_port=4506, pub_port=4505):
        '''
        The Salt Broker
        '''
        self.master = master
        self.ret_port = ret_port
        self.pub_port = pub_port

    def _ret_broker(self):
        '''
        Salt ret broker

        From: http://zguide.zeromq.org/py:msgqueue
        '''
        master_ret = "tcp://%s:%s" %(self.master, self.ret_port)
        context = zmq.Context()
        frontend = context.socket(zmq.ROUTER)
        frontend.bind("tcp://*:%s" %self.ret_port)
        backend = context.socket(zmq.DEALER)
        backend.connect(master_ret)
        zmq.device(zmq.QUEUE, frontend, backend)

    def _pub_broker(self):
        '''
        Salt publish broker

        From: http://zguide.zeromq.org/py:wuproxy
        '''
        master_pub = "tcp://%s:%s" %(self.master, self.pub_port)
        context = zmq.Context()
        frontend = context.socket(zmq.SUB)
        frontend.connect(master_pub)
        backend = context.socket(zmq.PUB)
        backend.bind("tcp://*:%s" %self.pub_port)
        frontend.setsockopt(zmq.SUBSCRIBE, b'')
        while True:
            message = frontend.recv_multipart()
            backend.send_multipart(message)

    def start(self):
        ret_broker = multiprocessing.Process(target=self._ret_broker)
        ret_broker.start()
        pub_broker = multiprocessing.Process(target=self._pub_broker)
        pub_broker.start()


if __name__ == '__main__':
    master = '192.168.1.1'    # should change to real master ip
    ret_port = 4506
    pub_port = 4505
    salt_broker = Broker(master, ret_port, pub_port)
    salt_broker.start()
