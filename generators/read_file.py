# -*- coding: utf-8 -*-
# @Author: ckochman
# @Date:   2017-05-04 17:11:27
# @Last Modified by:   ckochman
# @Last Modified time: 2017-05-04 17:11:31

def read_file(path):
    ''' reads a file into a line generator '''
    with open(path) as f:
        for line in f:
            yield line
