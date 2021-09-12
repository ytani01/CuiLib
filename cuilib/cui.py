#!/usr/bin/env python3
#
# Copyright (c) 2020 Yoichi Tanibayashi
#
"""
CUI library
"""
__author__ = 'Yoichi Tanibayashi'
__date__ = '2021/09'

import threading
from blessed import Terminal
from .my_logger import get_logger


class Cmd:  # pylint: disable=too-few-public-methods
    """ Cmd """
    def __init__(self, key_sym, func, help_str='', debug=False):
        """ Constructor

        Parameters
        ----------
        key_sym: list of str
        func: function
        help_str: str
        """
        self._dbg = debug
        self.__log = get_logger(self.__class__.__name__, self._dbg)
        self.__log.debug('%s:%s:%s', key_sym, func, help_str)

        self.key_sym = key_sym
        self.func = func
        self.help_str = help_str

    def __str__(self):
        """ str """
        out_str = '%a' % (self.key_sym)
        out_str += ':%s()' % (self.func.__name__)
        out_str += ':%s' % (self.help_str)
        return out_str


class Cui(threading.Thread):
    """ Cui """
    INKEY_TIMEOUT = 0.2

    def __init__(self, inkey_timeout=INKEY_TIMEOUT, debug=False):
        """ Constructor

        Parameters
        ----------
        inkey_timeout: float
            timeout sec of inkey()
        """
        self._dbg = debug
        self.__log = get_logger(self.__class__.__name__, self._dbg)

        self._cmd = []

        self._inkey_timeout = inkey_timeout
        self._active = False
        self._term = Terminal()

        super().__init__(daemon=True)

    def end(self, key_sym=None):
        """
        Call at the end of program

        Parameters
        ----------
        key_sym: None
            dummy to be used as command function
        """
        self.__log.debug('key_sym=%s: doing ..', key_sym)
        self._active = False
        self.join()
        self.__log.debug('done')

    def is_active(self):
        """
        """
        return self._active

    def add(self, key_sym, func, help_str=''):
        """
        add cmd

        Parameters
        ----------
        key_sym: str or list of str
            key symbols
        func: func
            command function
        help_str: str
            help string
        """
        if isinstance(key_sym, str):
            key_sym = list(key_sym)

        cmd = Cmd(key_sym, func, help_str, debug=self._dbg)
        self.__log.debug('cmd=%s', cmd)

        self._cmd.append(cmd)

    def help(self, key_sym=None, print_flag=True):
        """ command list

        Parameters
        ----------
        key_sym: None
            dummy to be used as command function

        print_flag: bool
            print or not

        Returns
        -------
        help_list: list of str
        """
        self.__log.debug('key_sym=%s', key_sym)

        help_list = []
        for cmd in self._cmd:
            help_str = '%a %s' % (cmd.key_sym, cmd.help_str)
            help_list.append(help_str)

        if print_flag:
            for help_str in help_list:
                print(help_str)

        return help_list

    def run(self):
        """
        run thread
        """
        self.__log.debug('run forever ..')

        self._active = True

        with self._term.cbreak():
            while self._active:
                inkey = self._term.inkey(timeout=self._inkey_timeout)

                if not inkey:
                    if self._dbg:
                        print('.', end='', flush=True)
                    continue

                if inkey.is_sequence:
                    inkey = inkey.name

                self.__log.debug('inkey=\'%s\'', inkey)

                call_flag = False
                for cmd in self._cmd:
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
                    self.__log.warning('invalid key: %a .. ignored', inkey)

        self.__log.debug('done')
