#
# (c) 2020 Yoichi Tanibayashi
#
"""
main for culib
"""
import time
import click
from . import Cui, CuiCmd
from .my_logger import get_logger


class SampleApp:
    """ Sample application class """

    def __init__(self, debug=False):
        """ Constructor """
        self._dbg = debug
        self.__log = get_logger(self.__class__.__name__, self._dbg)

        self._active = False

        self._cmd = [
            CuiCmd('aAあ', self.func1, debug=self._dbg),
            CuiCmd(['b', 'B', 'い'], self.func2, debug=self._dbg),
            CuiCmd(['q', 'Q', 'KEY_ESCAPE', '終'],
                   self.quit, debug=self._dbg)
        ]

        self._cui = Cui(self._cmd, debug=self._dbg)

    def func1(self, key_sym):
        """ func1 """
        self.__log.debug('key_sym=%s', key_sym)

        print('%s: start' % key_sym)
        time.sleep(2)
        print('%s: end' % key_sym)

    def func2(self, key_sym):
        """ func2 """
        self.__log.debug('key_sym=%s', key_sym)

        print('%s: start' % key_sym)
        time.sleep(1)
        print('%s: end' % key_sym)

    def quit(self, key_sym):
        """ quit """
        self.__log.debug('key_sym=%s', key_sym)

        print('%s: quit!' % key_sym)
        self._active = False

    def main(self):
        """ main """
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


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS, help='''
cuilib sample program
''')
@click.option('--debug', '-d', 'debug', is_flag=True, default=False,
              help='debug flag')
def main(debug):
    """ main for sample app """
    __log = get_logger(__name__, debug)

    app = SampleApp(debug=debug)
    try:
        app.main()
    finally:
        __log.debug('finally')
        app.end()


if __name__ == '__main__':
    main() # pylint: disable=no-value-for-parameter
