#!/usr/bin/env python3
#
# (c) 2021 Yoichi Tanibayashi
#
""" sample for cuilib """

import time
import cuilib

cui = cuilib.Cui(debug=True)
active = True

def func1(key_sym):
    print('func1:start')
    time.sleep(2)
    print('func1:end')

def func2(key_sym):
    print('func2:start')
    time.sleep(3)
    print('func2:end')

def help(key_sym):
    global cui
    cui.help(True)

def quit(key_sym):
    global cui
    cui.end()
    
cui.add('test', func1, 'func1')
cui.add('テスト', func2, 'func2')
cui.add('hH?', help, 'command help')
cui.add(['q', 'Q', 'KEY_ESCAPE', '\x04'], quit, 'quit') # '\x04'=[Ctrl]-D

cui.start()
cui.join()   # wait for quit
