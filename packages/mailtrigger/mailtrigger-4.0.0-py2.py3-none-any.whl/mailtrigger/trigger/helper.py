# -*- coding: utf-8 -*-

import os

from .trigger import Trigger
from ..registry import REGISTRY


class Helper(Trigger):
    def __init__(self, _):
        self._trigger = '@help'

    def _parse(self, event):
        lines = event['content'].splitlines()
        ret = False
        for item in lines:
            if self._trigger == item.strip():
                ret = True
                break
        return ret

    @staticmethod
    def help():
        return ''

    def run(self, event):
        if event is None or self._parse(event) is False:
            return 'Unsupported', False
        msg = []
        for item in REGISTRY:
            msg.append(item['class'].help())
        return os.linesep.join(msg), True
