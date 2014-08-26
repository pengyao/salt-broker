# -*- coding: utf-8 -*-

# Import python libs
import os

# Import salt libs
from salt.utils.parsers import OptionParserMeta, OptionParser, ConfigDirMixIn, \
    LogLevelMixIn, RunUserMixin, DaemonMixIn, PidfileMixin
import salt.syspaths as syspaths

import saltbroker.config as config

class BrokerOptionParser(OptionParser, ConfigDirMixIn, LogLevelMixIn,
    RunUserMixin, DaemonMixIn, PidfileMixin):

    __metaclass__ = OptionParserMeta

    description = 'The Salt broker, used to forward message between master and minions.'

    # ConfigDirMixIn config filename attribute
    _config_filename_ = 'broker'
    # LogLevelMixIn attribute
    _default_logging_logfile_ = os.path.join(syspaths.LOGS_DIR, 'broker')

    def setup_config(self):
        return config.broker_config(self.get_config_file_path())
