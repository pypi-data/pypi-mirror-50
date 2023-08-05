#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright @ 2014 Mitchell Chu

from __future__ import (absolute_import, division, print_function,
                        with_statement)

from datetime import datetime
import os
from os.path import exists, isdir, join

from torndsession.driver import SessionDriver
from torndsession.session import SessionConfigurationError

utcnow = datetime.utcnow
try:
    import cPickle as pickle    #  py2
except ImportError:
    import pickle               #  py3


class FileSession(SessionDriver):
    """
    System File to save session object.
    """
    #  default host is '#_sessions' directory which is in current directory.
    DEFAULT_SESSION_POSITION = './#_sessions'
    """
    Session file default save position.
    In a recommendation, you need give the host option.
    when host is missed, system will use this value by default.

    Additional @ Version: 1.1
    """

    def __init__(self, **settings):
        """
        Initialize File Session Driver.
        settings section 'host' is recommended, the option 'prefix' is an optional.
        if prefix is not given, 'default' is the default.
        host: where to save session object file, this is a directory path.
        prefix: session file name's prefix. session file like: prefix@session_id
        """
        super(FileSession, self).__init__(**settings)
        self.host = settings.get("host", self.DEFAULT_SESSION_POSITION)
        self._prefix = settings.get("prefix", 'default')
        if not exists(self.host):
            os.makedirs(self.host, 448)  #  only owner can visit this session directory.

        if not isdir(self.host):
            raise SessionConfigurationError('session host not found')

    def get(self, session_id):
        session_file = join(self.host, self._prefix + session_id)
        if not exists(session_file):
            return {}

        with open(session_file, 'rb') as rf:
            session = pickle.load(rf)

        now = utcnow()
        expires = session.get('__expires__', now)
        if expires > now:
            return session
        return {}

    def save(self, session_id, session_data, expires=None):
        session_file = join(self.host, self._prefix + session_id)
        session_data = session_data if session_data else {}

        if expires:
            session_data.update(__expires__=expires)
        with open(session_file, 'wb') as wf:
            pickle.dump(session_data, wf)

    def clear(self, session_id):
        session_file = join(self.host, self._prefix + session_id)
        if exists(session_file):
            os.remove(session_file)

    def remove_expires(self):
        if not exists(self.host) or not isdir(self.host): return
        now = utcnow()
        for session_file in os.listdir(self.host):
            if session_file.startswith(self._prefix):
                session_file = join(self.host, session_file)
                with open(session_file, 'rb') as sfile:
                    session = pickle.load(sfile)
                expires = session.get('__expires__', now)
                if expires <= now:
                    os.remove(session_file)
