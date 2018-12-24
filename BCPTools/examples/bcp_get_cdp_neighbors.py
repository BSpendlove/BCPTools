import sys
sys.path.append("..")

from BCPTFunctions import bcp_create_session
from BCPTFunctions import bcp_get_cdp_neighbors

from pprint import pprint
import os

conn = {
    'device_type': 'cisco_ios',
    'ip': '127.0.0.1', #Don't use this... just call the devices and run through a loop.. Have a look at the exam$
    'username': 'hume',
    'password': 'cisco',
    'secret': 'cisco'
}

devices = ['192.168.1.109']

for device in devices:
    print("Current device: {0}".format(device))
    conn.update({'ip':   device})

    session = bcp_create_session(conn)

    output = bcp_get_cdp_neighbors(session)
    for x in output:
        pprint(x['destination_host'])
