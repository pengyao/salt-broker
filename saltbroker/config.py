# -*- coding: utf-8 -*-

# Import python libs
import os

# Import salt libs
import salt
from salt.config import load_config

_DFLT_LOG_DATEFMT = '%H:%M:%S'
_DFLT_LOG_DATEFMT_LOGFILE = '%Y-%m-%d %H:%M:%S'
_DFLT_LOG_FMT_CONSOLE = '[%(levelname)-8s] %(message)s'
_DFLT_LOG_FMT_LOGFILE = (
    '%(asctime)s,%(msecs)03.0f [%(name)-17s][%(levelname)-8s] %(message)s'
)

DEFAULT_BROKER_OPTS = {
    'interface': '0.0.0.0',
    'master': 'salt',
    'ret_port': '4506',
    'publish_port': '4505',
    'ipv6': False,
    'user': 'root',
    'conf_file': os.path.join(salt.syspaths.CONFIG_DIR, 'minion'),
    'log_file': os.path.join(salt.syspaths.LOGS_DIR, 'broker'),
    'log_level': None,
    'log_datefmt': _DFLT_LOG_DATEFMT,
    'log_datefmt_logfile': _DFLT_LOG_DATEFMT_LOGFILE,
    'log_fmt_console': _DFLT_LOG_FMT_CONSOLE,
    'log_fmt_logfile': _DFLT_LOG_FMT_LOGFILE,
    'log_granular_levels': {},
    'extension_modules': '',
    'pidfile': os.path.join(salt.syspaths.PIDFILE_DIR, 'salt-broker.pid'),
}

def broker_config(path, env_var='SALT_BROKER_CONFIG', defaults=None):
    '''
    Reads in the broker configuration file and sets up default options
    '''
    if defaults is None:
        defaults = DEFAULT_BROKER_OPTS

    opts = {}
    opts.update(DEFAULT_BROKER_OPTS)
    if not os.environ.get(env_var, None):
        salt_config_dir = os.environ.get('SALT_CONFIG_DIR', None)
        if salt_config_dir:
            env_config_file_path = os.path.join(salt_config_dir, 'broker')
            if os.path.isfile(env_config_file_path):
                os.environ[env_var] = env_config_file_path

    opts.update(load_config(path, env_var, DEFAULT_BROKER_OPTS['conf_file']))
    return opts
