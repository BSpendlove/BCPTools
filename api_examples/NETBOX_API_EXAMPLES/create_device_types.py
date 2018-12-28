## Running this script will generate a load of cisco models within your device types in netbox...

from netbox import NetBox

myToken = 'mytoken123mytoken123mytoken123mytoken123'
api_login = NetBox(host='192.168.1.9', port=80, use_ssl=False, auth_token=myToken)
cisco_manufacturer = 2

#This function will pull the cisco switch models provided in the text file and create them as a 'device_type' in your netbox if you setup the API token + fill out the above variables
def create_cisco_switch_types(id_manufacturer=None, api=None):
    switches = open('cisco_switch_models.txt','r')
    #cisco_manufacturer = api_login.dcim.get_manufacturers()

    for switch in switches:
        output = api.dcim.create_device_type(model=switch,slug=switch,manufacturer=id_manufacturer, u_height=1,is_full_depth=False)
        print("\nCreating switch model: {0}\n".format(switch))
        print(output)

create_cisco_switch_types(cisco_manufacturer, api_login)

