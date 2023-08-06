# -*- coding: utf-8 -*-

import json
import os
import paramiko

from .trigger import Trigger, TriggerException

PREFIX = '@gerrit '

HELP = (
    PREFIX + 'abandon <host> <changenumber>',
    PREFIX + 'help',
    PREFIX + 'list',
    PREFIX + 'query <host> <changenumber>',
    PREFIX + 'rebase <host> <changenumber>',
    PREFIX + 'restart <host>',
    PREFIX + 'restore <host> <changenumber>',
    PREFIX + 'review <host> <changenumber>',
    PREFIX + 'reviewer <host> <changenumber> [add|remove] <reviewer>',
    PREFIX + 'start <host>',
    PREFIX + 'stop <host>',
    PREFIX + 'submit <host> <changenumber>',
    PREFIX + 'version <host>'
)


class Dispatcher(object):
    def __init__(self, config):
        self._client = paramiko.SSHClient()
        self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self._dispatcher = {
            'abandon': self._abandon,
            'help': self._help,
            'list': self._list,
            'query': self._query,
            'rebase': self._rebase,
            'restart': self._restart,
            'restore': self._restore,
            'review': self._review,
            'reviewer': self._reviewer,
            'start': self._start,
            'stop': self._stop,
            'submit': self._submit,
            'version': self._version
        }
        self._server = config.get('server', [])

    def _exec(self, cmd, host):
        def _exec_helper(host):
            buf = None
            for item in self._server:
                if host == item['host']:
                    buf = item
                    break
            return buf
        server = _exec_helper(host)
        if server is None:
            return 'Incorrect host %s' % host, False
        self._client.connect(hostname=server['host'], port=29418, username=server['user'], password=server['pass'])
        _, stdout, stderr = self._client.exec_command(cmd)
        out, err = stdout.read(), stderr.read()
        self._client.close()
        msg = out.decode() if len(err.decode()) == 0 else err.decode()
        status = True if len(err.decode()) == 0 else False
        return msg, status

    def _abandon(self, msg, name):
        host, change = msg.split()
        result, status = self._query(msg, name)
        if status is True:
            result = json.loads(result)
            msg, status = self._exec('gerrit review --abandon --message "Abandoned triggered by %s" %s,%s' % (name, change, result['currentPatchSet']['number']), host)
        msg = 'Change %s abandoned' % change if status is True else 'Change %s is not abandoned' % change
        return msg, status

    def _help(self, msg, name):
        global HELP
        return os.linesep.join(HELP), True

    def _list(self, msg, name):
        hosts = [item['host'] for item in self._server]
        return os.linesep.join(hosts), True

    def _query(self, msg, name):
        host, change = msg.split()
        msg, status = self._exec('gerrit query --all-reviewers --current-patch-set --files --format=JSON change:%s' % change, host)
        msg = msg[:msg.find('{"type":"stats","rowCount":1')] if status is True else 'Change %s is not queried'
        return msg, status

    def _rebase(self, msg, name):
        host, change = msg.split()
        result, status = self._query(msg, name)
        if status is True:
            result = json.loads(result)
            msg, status = self._exec('gerrit review --rebase --message "Rebased triggered by %s" %s,%s' % (name, change, result['currentPatchSet']['number']), host)
        msg = 'Change %s rebased' % change if status is True else 'Change %s is not rebased' % change
        return msg, status

    def _restart(self, msg, name):
        return 'Unsupported', False

    def _restore(self, msg, name):
        host, change = msg.split()
        result, status = self._query(msg, name)
        if status is True:
            result = json.loads(result)
            msg, status = self._exec('gerrit review --restore --message "Restored triggered by %s" %s,%s' % (name, change, result['currentPatchSet']['number']), host)
        msg = 'Change %s restored' % change if status is True else 'Change %s is not restored' % change
        return msg, status

    def _review(self, msg, name):
        host, change = msg.split()
        result, status = self._query(msg, name)
        if status is True:
            result = json.loads(result)
            msg, status = self._exec('gerrit review --autosubmit +1 --code-review +2 --presubmit-ready +1 --presubmit-verified +1 --verified +1 --message "Reviewed triggered by %s" %s,%s'
                                     % (name, change, result['currentPatchSet']['number']), host)
        msg = 'Change %s reviewed' % change if status is True else 'Change %s is not reviewed' % change
        return msg, status

    def _reviewer(self, msg, name):
        host, change, opt, reviewer = msg.split()
        result, status = self._query(' '.join([host, change]), name)
        if status is True:
            result = json.loads(result)
            msg, status = self._exec('gerrit set-reviewers --%s %s %s'
                                     % (opt, reviewer, result['id']), host)
        msg = 'Change %s reviewer set' % change if status is True else 'Change %s reviewer not set' % change
        return msg, status

    def _start(self, msg, name):
        return 'Unsupported', False

    def _stop(self, msg, name):
        return 'Unsupported', False

    def _submit(self, msg, name):
        host, change = msg.split()
        result, status = self._query(msg, name)
        if status is True:
            result = json.loads(result)
            msg, status = self._exec('gerrit review --submit --message "Submitted triggered by %s" %s,%s'
                                     % (name, change, result['currentPatchSet']['number']), host)
        msg = 'Change %s submitted ' % change if status is True else 'Change %s is not submitted' % change
        return msg, status

    def _version(self, msg, name):
        host = msg
        msg, status = self._exec('gerrit version', host)
        msg = msg if status is True else 'Version not found'
        return msg, status

    def run(self, msg, name):
        msg = msg.split()
        buf = ' '.join(msg[1:]) if len(msg) > 1 else ''
        return self._dispatcher[msg[0]](buf, name)


class Gerrit(Trigger):
    def __init__(self, config):
        if config is None:
            raise TriggerException('invalid gerrit configuration')
        self._debug = config.get('debug', False)
        self._dispatcher = Dispatcher(config)
        self._server = config.get('server', [])

    def _dispatch(self, event):
        global PREFIX
        lines = event['content'].split('\n')
        msg = []
        for item in lines:
            item = item.strip()
            if len(item) == 0:
                continue
            buf = item.split()
            if buf[0] != PREFIX.strip() or len(buf) < 2:
                continue
            _msg, _ = self._dispatcher.run(' '.join(buf[1:]), event['from'])
            msg.append(_msg)
        if len(msg) != 0:
            msg = os.linesep.join(msg)
            status = True
        else:
            msg = 'Failed to dispatch event'
            status = False
        return msg, status

    @staticmethod
    def help():
        global HELP
        return os.linesep.join(HELP)

    def run(self, event):
        if event is None:
            return 'Unsupported', False
        return self._dispatch(event)
