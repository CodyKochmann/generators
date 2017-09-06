# -*- coding: utf-8 -*-
# @Author: ckochman
# @Date:   2017-05-04 17:11:54
# @Last Modified by:   ckochman
# @Last Modified time: 2017-05-04 18:06:21

import sys

def script_path(include_name=False):
    # returns the full path of the script containing this snippet
    from os import path
    full_path = path.realpath(__file__)
    if include_name:
        return(full_path)
    else:
        full_path = "/".join( full_path.split("/")[0:-1] ) + "/"
        return(full_path)

sys.path.append(script_path())


from average import average
from counter import counter
from fork import fork
from itemgetter import itemgetter
from multi_ops import multi_ops
from read_file import read_file
from started import started
from timer import timer
from total import total
from unfork import unfork

