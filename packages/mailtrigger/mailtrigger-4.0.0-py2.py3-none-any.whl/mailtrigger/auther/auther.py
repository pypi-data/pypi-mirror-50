# -*- coding: utf-8 -*-


class AutherException(Exception):
    def __init__(self, info):
        super().__init__(self)
        self._info = info

    def __str__(self):
        return self._info


class Auther(object):
    def __init__(self, config):
        if config is None:
            raise AutherException('invalid auther configuration')
        self._debug = config.get('debug', False)
        self._group = config.get('group', None)
        self._message = config.get('message', None)
        self._provider = config.get('provider', None)

    def _auth_group(self, event):
        if self._group is None:
            return False
        status = False
        for group, members in self._group.items():
            if group.startswith('ldap/'):
                # TODO
                pass
            if event['from'] in members:
                status = True
                break
        return status

    def _auth_message(self, event):
        if self._message is None:
            return False
        subject = self._message.get('subject', '').strip()
        if len(subject) == 0 or event['subject'].startswith(subject) is False:
            return False
        return True

    def auth(self, event):
        if event is None:
            return 'Unsupported', False
        if self._auth_group(event) is False or self._auth_message(event) is False:
            return 'Unauthorized', False
        return 'Authorized', True
