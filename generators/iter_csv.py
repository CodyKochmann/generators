# -*- coding: utf-8 -*-
# @Author: Cody Kochmann
# @Date:   2017-12-09 10:03:01
# @Last Modified by:   Cody Kochmann
# @Last Modified time: 2017-12-09 11:16:46

from csv import DictReader
from strict_functions import strict_globals


@strict_globals(DictReader=DictReader)
def iter_csv(path, mode='r'):
    with open(path, mode) as f:
        for row in DictReader(f):
            yield dict(row)

del DictReader, strict_globals


if __name__ == '__main__':
    c = iter_csv('/Users/cody/Desktop/Traffic_Violations.csv')
    print(next(c))
