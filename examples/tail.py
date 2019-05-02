# -*- coding: utf-8 -*-
# @Author: Cody Kochmann
# @Date:   2019-05-01 07:54:28
# @Last Modified by:   Cody Kochmann
# @Last Modified time: 2019-05-02 13:24:38

""" This demonstrates how you can use generator pipelines to implement tail in
    pure python.
"""

import os
from typing import Iterable

# this example does require you to have inotify installed
try:
    import inotify.adapters
except ImportError:
    raise ImportError('''
        this example requires that you have "inotify" installed so python
        can watch for file events. If you're using pip, "pip install inotify"
        is all you need!
    ''')
from generators import Generator as G

def tail(file_path:str) -> Iterable[str]:
    assert os.path.isfile(file_path)

    notifier = inotify.adapters.Inotify()
    notifier.add_watch(file_path)

    with open(file_path, 'r') as f:
        notifier.add_watch(file_path)

        yield from G(  # create a Generator fed by the notifier
            notifier.event_gen(yield_nones=False)
        ).filter(  # filter for IN_MODIFY events (mask equals 2)
            lambda i: i[0].mask == 2
        ).map(  # when the file is modified, get the new size
            lambda i: os.path.getsize(i[2])
        ).uniq(  # filter duplicates, just incase nothing was added to the file
        ).window(  # window the (previous_size, current_size)
            2
        ).side_task(  # seek the file descriptor and pass the input since f.seek returns None
            lambda i: f.seek(i[0])
        ).map(  # read in the newly added data
            lambda i: f.read(i[1]-i[0])
        ).chain(  # chain the incoming chunks since they might not be single lines
        ).groupby(  # seperate groups by lines
            lambda i:i=='\n'
        ).filter(  # exclude groups that are just '\n', since they are the delimiters
            lambda i:i[0]==False
        ).map(  # join the characters to construct each line as a string
            lambda i:''.join(i[1])
        #).print('-', use_repr=True  # uncomment this line to see the constructed lines
        )

if __name__ == '__main__':
    from sys import argv

    for line in tail(argv[-1]):
        print(line.strip())
