#!/usr/bin/env python3
#
# (c) 2021 Yoichi Tanibayashi
#
""" sample for cuilib """

import time
import cuilib


def func1(key_sym):
    print('func1:start')
    time.sleep(2)
    print('func1:end')


def func2(key_sym):
    print('func2:start')
    time.sleep(3)
    print('func2:end')


if __name__ == '__main__':
    cui = cuilib.Cui()

    cui.add('test', func1, 'func1')
    cui.add('テスト', func2, 'func2')
    cui.add('hH?', cui.help, 'command help')
    cui.add(['q', 'Q', 'KEY_ESCAPE', '\x04'],
            cui.end, 'quit')  # '\x04'=[Ctrl]-D

    cui.start()
    cui.join()   # wait for quit
