# -*- coding: utf-8 -*-
# @Author: Cody Kochmann
# @Date:   2018-02-17 14:39:01
# @Last Modified by:   Cody Kochmann
# @Last Modified time: 2018-02-17 15:00:00

from loop import loop
from started import started

@started
def remember():
    ''' this coroutine remembers one thing for you and acts as a read-once method
        of transportation for code. This makes obcessive cleanup of variables a
        lot easier.
    '''
    a = None
    b = None
    for _ in loop():
        b = yield b
        a = yield a

if __name__ == '__main__':
    member = remember()
    print('sending 3 -', member.send(3))
    print('sending 5 -', member.send(5))
    print('retrieving 5 -', next(member))
    print(next(member))
    print(next(member))
