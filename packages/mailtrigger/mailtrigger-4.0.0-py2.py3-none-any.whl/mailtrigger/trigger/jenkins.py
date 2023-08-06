# -*- coding: utf-8 -*-

from .trigger import Trigger, TriggerException


class Jenkins(Trigger):
    def __init__(self, config):
        if config is None:
            raise TriggerException('invalid jenkins configuration')
        self._debug = config.get('debug', False)

    @staticmethod
    def help():
        return ''

    def run(self, event):
        if event is None:
            return 'Unsupported', False
        return 'Unsupported', False
