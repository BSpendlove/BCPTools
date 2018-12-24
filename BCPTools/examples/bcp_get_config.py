from BCPTools.BCPTFunctions import bcp_create_session
from BCPTools.BCPTFunctions import bcp_get_config

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

    bcp_get_config(session,True) #Specify False to keep passwords in configuration files... If you don't specify anything, then your passwords will be replaced in the backup file with '<removed>'
    print("Complete!")
