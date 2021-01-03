#!/usr/bin/env python3
#
# (c) 2021 Yoichi Tanibayashi
#
""" sample for cuilib """

import sys
import time
import cuilib

debug_flag=False
if len(sys.argv) > 1:
    debug_flag=True

cui = cuilib.Cui(debug=debug_flag)
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
    global active

    print('quit:start')
    active = False
    print('quit:end')
    
cui.add('test', func1, 'func1')
cui.add('テスト', func2, 'func2')
cui.add('hH?', help, 'command help')
cui.add(['q', 'Q', 'KEY_ESCAPE', '\x04'], quit, 'quit') # '\x04': Ctrl-D

cui.start()

while active:
    time.sleep(.2)

cui.end()
