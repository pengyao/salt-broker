# -*- coding: utf-8 -*-

# Import python libs
import logging

# Import third party libs
import zmq

log = logging.getLogger(__name__)

def set_tcp_keepalive(sock, opts=None):
    # Warn if ZMQ < 3.2
    try:
        zmq_version_info = zmq.zmq_version_info()
    except AttributeError:
        # PyZMQ <= 2.1.9 does not have zmq_version_info, fall back to
        # using zmq.zmq_version() and build a version info tuple.
        zmq_version_info = tuple(
            [int(x) for x in zmq.zmq_version().split('.')]
        )
    if zmq_version_info < (3, 2):
        log.warning(
            'You have a version of ZMQ less than ZMQ 3.2! There are '
            'known connection keep-alive issues with ZMQ < 3.2 which '
            'may result in loss of contact with minions. Please '
            'upgrade your ZMQ!'
        )

    if hasattr(zmq, 'TCP_KEEPALIVE') and opts:
        if 'tcp_keepalive' in opts:
            sock.setsockopt(
                zmq.TCP_KEEPALIVE, opts['tcp_keepalive']
            )
        if 'tcp_keepalive_idle' in opts:
            sock.setsockopt(
                zmq.TCP_KEEPALIVE_IDLE, opts['tcp_keepalive_idle']
            )
            if 'tcp_keepalive_cnt' in opts:
                sock.setsockopt(
                    zmq.TCP_KEEPALIVE_CNT, opts['tcp_keepalive_cnt']
                )
            if 'tcp_keepalive_intvl' in opts:
                sock.setsockopt(
                    zmq.TCP_KEEPALIVE_INTVL, opts['tcp_keepalive_intvl']
                )
    return sock

