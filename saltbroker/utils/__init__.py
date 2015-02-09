# -*- coding: utf-8 -*-
'''
Some of the utils used by salt broker
'''

# Import python libs
import logging
import os
import time
import signal

try:
    import setproctitle
    HAS_SETPROCTITLE = True
except ImportError:
    HAS_SETPROCTITLE = False

log = logging.getLogger(__name__)

def clean_proc(proc, wait_for_kill=10):
    '''
    Generic method for cleaning up multiprocessing procs

    From: https://github.com/saltstack/salt/blob/v2014.1.13/salt/master.py#L74
    '''
    # NoneType and other fun stuff need not apply

    if not proc:
        return
    try:
        waited = 0
        while proc.is_alive():
            proc.terminate()
            waited += 1
            time.sleep(0.1)
            if proc.is_alive() and (waited >= wait_for_kill):
                log.error(
                    'Process did not die with terminate(): {0}'.format(
                        proc.pid
                    )
                )
                os.kill(signal.SIGKILL, proc.pid)
    except (AssertionError, AttributeError):
        # Catch AssertionError when the proc is evaluated inside the child
        # Catch AttributeError when the process dies between proc.is_alive()
        # and proc.terminate() and turns into a NoneType
        pass


def appendproctitle(name):
    '''
    Append "name" to the current process title

    From: https://github.com/saltstack/salt/blob/v2014.7.1/salt/utils/__init__.py#L2377
    '''
    if HAS_SETPROCTITLE:
        setproctitle.setproctitle(setproctitle.getproctitle() + ' ' + name)
