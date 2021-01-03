#!/usr/bin/env python3
#
# (c) 2020 Yoichi Tanibayashi
#
"""
CUI library
"""
__author__ = 'Yoichi Tanibayashi'
__date__ = '2021/01'

import threading
from blessed import Terminal
from my_logger import get_logger


class CuiCmd:  # pylint: disable=too-few-public-methods
    """ CuiCmd """
    def __init__(self, key_sym, func, debug=False):
        """ Constructor
        """
        self._dbg = debug
        self.__log = get_logger(self.__class__.__name__, self._dbg)

        self.key_sym = key_sym
        self.func = func


class Cui(threading.Thread):
    """ Cui """
    INKEY_TIMEOUT = 0.5

    def __init__(self, cmd, debug=False):
        """ Constructor

        Parameters
        ----------
        cmds: list of CuiCmd
        """
        self._dbg = debug
        self.__log = get_logger(self.__class__.__name__, self._dbg)

        if type(cmd) != list or type(cmd[0]) != CuiCmd:
            err = ValueError('invalid cmd list: %s' % cmd)
            raise err

        self._cmd = cmd

        self._active = False
        self._term = Terminal()

        super().__init__(daemon=True)

    def end(self):
        """
        Call at the end of program
        """
        self.__log.debug('doing ..')
        self._active = False
        self.join()
        self.__log.debug('done')

    def run(self):
        """
        run thread
        """
        self.__log.debug('run forever ..')

        self._active = True

        with self._term.cbreak():
            while self._active:
                inkey = self._term.inkey(timeout=self.INKEY_TIMEOUT)

                if not inkey:
                    self.__log.debug('waiting key input ..')
                    continue

                if inkey.is_sequence:
                    inkey = inkey.name

                self.__log.debug('inkey=%s', inkey)

                call_flag = False
                for cmd in self._cmd:
                    if isinstance(cmd.key_sym, str):
                        cmd.key_sym = list(cmd.key_sym)

                    for sym in cmd.key_sym:
                        if sym == inkey:
                            call_th = threading.Thread(target=cmd.func,
                                                       args=(sym,),
                                                       daemon=True)
                            call_th.start()

                            call_flag = True
                            break

                    if call_flag:
                        break

                if not call_flag:
                    self.__log.debug('invalid key: %a .. ignored', inkey)

        self.__log.debug('done')
