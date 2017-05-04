# -*- coding: utf-8 -*-
# @Author: ckochman
# @Date:   2017-05-04 16:44:16
# @Last Modified by:   ckochman
# @Last Modified time: 2017-05-04 16:44:31


def started(generator_function):
    """ starts a generator when created """
    def wrapper(*args, **kwargs):
        g = generator_function(*args, **kwargs)
        next(g)
        return g
    return wrapper
