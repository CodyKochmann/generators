# -*- coding: utf-8 -*-
# @Author: ckochman
# @Date:   2017-05-04 16:44:16
# @Last Modified by:   Cody Kochmann
# @Last Modified time: 2017-12-09 13:23:24

from functools import wraps
from strict_functions import strict_globals

@strict_globals(wraps=wraps)
def started(generator_function):
    """ starts a generator when created """
    @wraps(generator_function)
    def wrapper(*args, **kwargs):
        g = generator_function(*args, **kwargs)
        next(g)
        return g
    return wrapper

del strict_globals, wraps
