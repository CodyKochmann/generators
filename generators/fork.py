# -*- coding: utf-8 -*-
# @Author: ckochman
# @Date:   2017-05-04 18:03:54
# @Last Modified by:   ckochman
# @Last Modified time: 2017-05-04 18:04:05

def fork(g,c=2):
    """ fork a generator in python """
    return ((i,)*c for i in g)
