# -*- coding: utf-8 -*-

# Import python libs

# Import salt libs
import salt.log.setup
from salt.utils.verify import check_user

import saltbroker.broker
from saltbroker.utils import parsers

logger = salt.log.setup.logging.getLogger(__name__)


class Broker(parsers.BrokerOptionParser):
    '''
    Create a broker server
    '''
    def prepare(self):
        self.parse_args()

        self.setup_logfile_logger()
        logger.info('Setting up Salt Broker')

        self.daemonize_if_required()
        self.set_pidfile()
        self.broker = saltbroker.broker.Broker(self.config)

    def start(self):
        '''
        Start broker.
        '''
        self.prepare()
        if check_user(self.config['user']):
            self.broker.start()

    def shutdown(self):
        '''
        Shutdown
        '''
