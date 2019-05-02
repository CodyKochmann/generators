# -*- coding: utf-8 -*-
# @Author: Cody Kochmann
# @Date:   2019-05-02 13:20:11
# @Last Modified by:   Cody Kochmann
# @Last Modified time: 2019-05-02 14:26:50

''' This example shows you how you can use generators to make code that scrapes
    html a lot less bloated.

    This script in specific is a little tool I threw together to use to extract
    urls from a webpage.

    Example Usage:

        python scrape_urls.py https://google.com

'''

from sys import argv
from string import printable

from generators import G

# this example does require you to have requests installed
try:
    from requests import get
except ImportError:
    raise ImportError('''
        this example requires that you have "requests" installed so python
        can watch for file events. If you're using pip, "pip install requests"
        is all you need!
    ''')

# this makes a bytestring of the printable chatacters we normally care about for
# easier input sanitization.
printable_bytes = printable.encode()


def scrape_urls(target):
    return G(  # create a generator that iterates over the target url's content
        get(target).iter_content()
    ).filter(  # clean the incoming data to just printables
        lambda char: char in printable_bytes
    ).groupby(  # create groups by seperating the content by its quotes
        lambda char: char in {b'"', b"'"}
    ).map(  # join the bytes between quotes and encode them to strings
        lambda flag_group: b''.join(flag_group[1]).decode()
    ).filter(  # filter for relative and non-relative urls
        lambda s: (s.startswith('/') or '://' in s) and ' ' not in s
    ).map(  # add target to the beginning of relative urls
        lambda url: target.strip('/') + url if url.startswith('/') else url
    # ).print('found:'  # uncomment this line to see all urls the script is finding before deduplication
    ).to(set)


if __name__ == '__main__':
    # uncomment this line for non-cli testing
    #argv.append('https://google.com')

    # last cli argument is the target url
    target_url = argv[-1]

    assert '://' in target_url, 'this does not seem to be a url: {}'.format(target_url)

    for url in scrape_urls(target_url):
        print(url)
