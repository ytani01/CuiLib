#!/usr/bin/env python3
#
# (c) 2020 Yoichi Tanibayashi
#
"""
Python3 template

### for detail and simple usage ###

$ python3 -m pydoc CuiUtil.CuiKey


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

    def __init__(self, key_sym, func, debug=False):
        """ Constructor
        """
        self._dbg = debug
        __class__.__log = get_logger(__class__.__name__, self._dbg)

        self.key_sym = key_sym
        self.func = func


class CuiKey(threading.Thread):
    """
    Description
    -----------

    Simple Usage
    ============
    from CuiUtil import CuiKey

    def func1(key_sym):
        print(key_sym)

    def func2(key_sym):
        print(key_sym)

    cmds = [
        CuiCmd('KeySym1', func1),
        CuiCmd('KeySym2', func2)
    ]

    cui = CuiKey(cmds)
    cui.start()  # run forever


    cur.end()  # call at the end of usage
    ============

    Attributes
    ----------
    attr1: type(int|str|list of str ..)
        description
    """
    INKEY_TIMEOUT = 0.5

    __log = get_logger(__name__, False)

    def __init__(self, cmd, debug=False):
        """ Constructor

        Parameters
        ----------
        cmds: list of CuiCmd
        """
        self._dbg = debug
        __class__.__log = get_logger(__class__.__name__, self._dbg)

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
                for c in self._cmd:
                    if type(c.key_sym) is str:
                        c.key_sym = list(c.key_sym)

                    for k in c.key_sym:
                        if k == inkey:
                            call_th = threading.Thread(target=c.func,
                                                       args=(inkey,),
                                                       daemon=True)
                            call_th.start()

                            call_flag = True
                            break

                    if call_flag:
                        break

                if not call_flag:
                    self.__log.debug('invalid key: %a .. ignored',
                                     inkey)

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

        self._active = False
        self._cmd = [
            CuiCmd('aA', self.func1, debug=self._dbg),
            CuiCmd(['b', 'B'], self.func2, debug=self._dbg),
            CuiCmd(['q', 'Q', 'KEY_ESCAPE'],
                   self.quit, debug=self._dbg)
        ]

        self._cui = CuiKey(self._cmd, debug=self._dbg)
        # self._cui = CuiKey([3], debug=self._dbg)

    def func1(self, key_sym):
        """
        """
        print('%s: start' % key_sym)
        time.sleep(2)
        print('%s: end' % key_sym)

    def func2(self, key_sym):
        """
        """
        print('%s: start' % key_sym)
        time.sleep(1)
        print('%s: end' % key_sym)

    def quit(self, key_sym):
        """
        """
        print('%s: quit!' % key_sym)
        self._active = False

    def main(self):
        """ main routine
        """
        self.__log.debug('')

        self._cui.start()

        self._active = True

        while self._active:
            time.sleep(1)

    def end(self):
        """ Call at the end of program.
        """
        self.__log.debug('doing ..')
        self._cui.end()
        self.__log.debug('done')


import click
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS, help='''
CuiUtil sample program
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
