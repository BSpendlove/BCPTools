import sys
sys.path.append("..")

#DEV Imports (not installing the module with pip)
from BCPTFunctions import bcp_create_session
from BCPTFunctions import bcp_show_vlans

#from BCPTools.BCPTFunctions import bcp_create_session
#from BCPTools.BCPTFunctions import bcp_show_vlans

import os
from pprint import pprint

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

    output = bcp_show_vlans(session)
    for vlan in output:
        pprint(vlan)
