# -*- coding: utf-8 -*-
'''
Some of the utils used by salt broker
'''

try:
    import setproctitle
    HAS_SETPROCTITLE = True
except ImportError:
    HAS_SETPROCTITLE = False


def appendproctitle(name):
    '''
    Append "name" to the current process title

    From: https://github.com/saltstack/salt/blob/v2014.7.1/salt/utils/__init__.py#L2377
    '''
    if HAS_SETPROCTITLE:
        setproctitle.setproctitle(setproctitle.getproctitle() + ' ' + name)
