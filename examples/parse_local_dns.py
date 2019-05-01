# -*- coding: utf-8 -*-
# @Author: Cody Kochmann
# @Date:   2019-05-01 08:50:41
# @Last Modified by:   Cody Kochmann
# @Last Modified time: 2019-05-01 09:21:48

'''
    This example is a little snippet I use every now and then to materialize
    the /etc/hosts file in linux to produce a dictionary with the following
    structure:

        {
            "localhost": "127.0.0.1",
            "hostname.com": "1.2.3.4"
        }
'''

from ipaddress import ip_address

from generators import Generator as G

def valid_ip(s: str) -> bool:
    try:
        ip_address(s)
        return True
    except:
        return False

host_dns = G(  # iterate over
    open('/etc/hosts', 'r')
).map(  # strip trailing whitespace
    str.strip
).filter(  # remove empty lines
    bool
).map(  # replace tabs with spaces, split remaining lines by spaces and filter empty strings
    lambda line: [field for field in line.replace('\t', ' ').split(' ') if field]
).filter(  # only lines that start with a valid ip address and have at least one following hostname
    lambda fields: valid_ip(fields[0]) and len(fields) > 1
).map(  # map every hostname on the line to the ip address
    lambda fields: [[hostname, fields[0]] for hostname in fields[1:]]
).chain(  # chain the lists so you have one long k,v stream
#).print(  # uncomment this line to see the k,v pairs be materialized
).to(dict)

if __name__ == '__main__':

    print(host_dns)
