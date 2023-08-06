# -*- coding: utf-8 -*-

import html2text
import poplib
import socket

from email.header import decode_header
from email.parser import Parser
from email.utils import parseaddr
from email.utils import parsedate
from ..logger.logger import Logger


class ReceiverException(Exception):
    def __init__(self, info):
        super().__init__(self)
        self._info = info

    def __str__(self):
        return self._info


class Receiver(object):
    def __init__(self, config):
        self._debug = config['debug']
        self._pop3 = config.get('pop3', None)
        if self._pop3 is None:
            raise ReceiverException('missing pop3 configuration')
        self._server = None

    def _connect(self):
        ssl = self._pop3.get('ssl', False)
        if ssl is True:
            self._server = poplib.POP3_SSL(host=self._pop3.get('host', ''), port=self._pop3.get('port', ''),
                                           timeout=self._pop3.get('timeout', 0))
        else:
            self._server = poplib.POP3(host=self._pop3.get('host', ''), port=self._pop3.get('port', ''),
                                       timeout=self._pop3.get('timeout', 0))
        if self._debug is True:
            self._server.set_debuglevel(1)
        else:
            self._server.set_debuglevel(0)
        self._server.user(self._pop3.get('user', ''))
        self._server.pass_(self._pop3.get('pass', ''))

    @staticmethod
    def _parse(msg):
        def _decode(msg):
            value, charset = decode_header(msg)[0]
            if charset:
                value = value.decode(charset)
            return value

        def _guess(msg):
            charset = msg.get_charset()
            if charset is None:
                ctype = msg.get('Content-Type', '').lower()
                pos = ctype.find('charset=')
                if pos >= 0:
                    charset = ctype[pos + 8:].strip()
            return charset

        def _content(msg):
            content = msg.get_payload(decode=True)
            charset = _guess(msg)
            if charset:
                content = content.decode(charset)
            return html2text.html2text(content)

        def _date(msg):
            if 'Date' not in msg:
                return ''
            year, month, date, hour, minute, second, _, _, _ = parsedate(msg['Date'])
            return '%s-%s-%s-%s-%s-%s' % (year, month, date, hour, minute, second)

        def _from(msg):
            _, addr = parseaddr(msg.get('From', ''))
            return addr

        def _subject(msg):
            return _decode(msg.get('Subject', ''))

        def _to(msg):
            _, addr = parseaddr(msg.get('To', ''))
            return addr

        content = ''
        msg = Parser().parsestr(msg)
        if msg.is_multipart():
            parts = msg.get_payload()
            found = False
            for _, part in enumerate(parts):
                if part.get_content_type() == 'text/html':
                    content = _content(part)
                    found = True
                    break
            if found is False:
                raise ReceiverException('required to html type')
        else:
            content = _content(msg)

        return {
            'content': content,
            'date': _date(msg),
            'from': _from(msg),
            'subject': _subject(msg),
            'to': _to(msg)
        }

    def connect(self):
        try:
            self._connect()
        except (OSError, poplib.error_proto, socket.timeout) as _:
            raise ReceiverException('failed to connect pop3 server')
        Logger.debug('connected to %s' % self._pop3.get('host', ''))

    def disconnect(self):
        if self._server is None:
            return
        try:
            self._server.quit()
        except (AttributeError, OSError, poplib.error_proto) as _:
            Logger.debug('failed to disconnect pop3 server')
            return
        Logger.debug('disconnected from %s' % self._pop3.get('host', ''))

    def receive(self, num):
        if self._server is None:
            raise ReceiverException('required to connect pop3 server')
        buf = []
        _, mails, _ = self._server.list()
        start = len(mails)
        stop = start - (num if num < len(mails) else len(mails))
        for index in range(start, stop, -1):
            _, lines, _ = self._server.retr(index)
            buf.append(self._parse(b'\n'.join(lines).decode('utf-8')))
        if len(buf) == 0:
            return None
        elif len(buf) == 1:
            return buf[0]
        return buf

    def stat(self):
        if self._server is None:
            raise ReceiverException('required to connect pop3 server')
        count, size = self._server.stat()
        return count, size
