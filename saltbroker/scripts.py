# -*- coding: utf-8 -*-
'''
This module contains the function calls to execute command line scipts
'''

# Import salt libs
import saltbroker

def salt_broker():
    '''
    Start the salt broker
    '''
    broker = saltbroker.Broker()
    broker.start()