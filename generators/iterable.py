# -*- coding: utf-8 -*-
# @Author: Cody Kochmann
# @Date:   2017-09-30 22:09:35
# @Last Modified by:   Cody Kochmann
# @Last Modified time: 2017-09-30 22:11:35

def iterable(target):
    ''' returns true if the given argument is iterable '''
    if any(i in ('next', '__next__', '__iter__') for i in dir(target)):
        return True
    else:
        try:
            iter(target)
            return True
        except:
            return False

