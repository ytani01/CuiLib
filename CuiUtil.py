#!/usr/bin/env python3
#
# (c) 2020 Yoichi Tanibayashi
#
"""
Python3 template

### for detail and simple usage ###

$ python3 -m pydoc CuiUtil.CuiBase


### sample program ###

$ ./CuiUtil.py -h


"""
__author__ = 'Yoichi Tanibayashi'
__date__   = '2020'

import threading
from blessed import Terminal
from MyLogger import get_logger


class CuiCmd:
    """
    """
    __log = get_logger(__name__, False)

    def __init__(self, key, func, debug):
        """ Constructor
        """
        self._dbg = debug
        __class__.__log = get_logger(__class__.__name__, self._dbg)

        self.key = key
        self.func = func


class CuiBase(threading.Thread):
    """
    Description
    -----------

    Simple Usage
    ============
    from CuiUtil import CuiBase

    def func1(key_sym):
        print(key_sym)

    def func2(key_sym):
        print(key_sym)

    cmds = [
        CuiCmd('KeySym1', func1),
        CuiCmd('KeySym2', func2)
    ]

    cui = CuiBase(cmds)
    cui.start()  # run forever


    cur.end()  # call at the end of usage
    ============

    Attributes
    ----------
    attr1: type(int|str|list of str ..)
        description
    """
    __log = get_logger(__name__, False)

    def __init__(self, cmd, debug=False):
        """ Constructor

        Parameters
        ----------
        cmds: list of Cmd
            description
        """
        self._dbg = debug
        __class__.__log = get_logger(__class__.__name__, self._dbg)

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

        while self._active:
            inkey = t.inkey(timeout=1)

            if not inkey:
                self.__log.debug('waiting key input ..')
                continue

            if inkey.is_sequence:
                self.__warning('inkey.name=%s .. ignored', inkey.name)
                continue

            self.__log.debug('inkey=%s', inkey)

            for c in self._cmd:
                if c.key == inkey:
                    c.func()

        self.__log.debug('done')


# --- 以下、サンプル ---


import time


class SampleApp:
    """ Sample application class

    Attributes
    ----------
    """
    __log = get_logger(__name__, False)

    def __init__(self, arg, opt, debug=False):
        """constructor

        Parameters
        ----------
        arg: str
            description
        opt: str
            description
        """
        self._dbg = debug
        __class__.__log = get_logger(__class__.__name__, self._dbg)
        self.__log.debug('arg=%s, opt=%s', arg, opt)

        self._arg = arg
        self._opt = opt

        cmd = [
            CuiCmd('a', self.func1),
            CuiCmd('b', self.func2)
        ]

        self._cui = CuiBase(self._opt, debug=self._dbg)

    def func1(self):
        """
        """
        print('func1: start')
        time.sleep(2)
        print('func1: end')

    def func2(self):
        """
        """
        print('func2: start')
        time.sleep(1)
        print('func2: end')

    def main(self):
        """ main routine
        """
        self.__log.debug('')
        self._cui.start()

    def end(self):
        """ Call at the end of program.
        """
        self.__log.debug('doing ..')
        self._cui.end()
        self.__log.debug('done')


import click
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS, help='''
CuiBase sample program
''')
@click.argument('arg', type=str, nargs=-1)
@click.option('--opt', '-o', 'opt', type=str, default='def_value',
              help='sample option: default=%s' % 'def_value')
@click.option('--debug', '-d', 'debug', is_flag=True, default=False,
              help='debug flag')
def main(arg, opt, debug):
    """サンプル起動用メイン関数
    """
    __log = get_logger(__name__, debug)
    __log.debug('arg=%s, opt=%s', arg, opt)

    app = SampleApp(arg, opt, debug=debug)
    try:
        app.main()
    finally:
        __log.debug('finally')
        app.end()


if __name__ == '__main__':
    main()
