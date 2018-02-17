# -*- coding: utf-8 -*-
# @Author: Cody Kochmann
# @Date:   2018-02-17 10:42:15
# @Last Modified by:   Cody Kochmann
# @Last Modified time: 2018-02-17 12:02:24

from skip import skip

def skip_first(pipe, items=1):
    ''' this is an alias for skip to parallel the dedicated skip_last function
        to provide a little more readability to the code. the action of actually
        skipping does not occur until the first iteration is done
    '''
    pipe = iter(pipe)
    for i in skip(pipe, items):
        yield i

if __name__ == '__main__':
    l = list(range(10))
    print(l)
    for i in skip_first(l, 5):
        print(i)
