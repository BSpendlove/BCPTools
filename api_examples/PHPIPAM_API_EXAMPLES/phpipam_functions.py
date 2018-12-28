#
#   This FILE is more of a documentation and testing for me when I tried using the functions in the phpipamsdk python module... I wouldn't recommend using them, but they give you some examples like adding vlan domains, vlans, subnets etc...
#

import warnings
import phpipamsdk #Import the library

from phpipamsdk.utils import get_subnet_id #Gets the local ID of the subnet
from phpipamsdk.utils import get_section_id #Gets the local ID of the section

from netmiko import ConnectHandler #Netmiko SSH Connection Handler

""" --------------- GLOBAL VARIABLES --------------- """

deviceType = 'cisco_ios'
ipAddr = '127.0.0.1'
usr = 'admin'
pwd = 'admin'
enable = pwd

conn = {
    'device_type': deviceType,
    'ip':   ipAddr,
    'username': usr,
    'password': pwd,
    'secret': enable,
}

devices = ['192.168.1.52']

""" ------------------------------------------------ """

def get_all_subnets(ipam_conn=None, py_section=None):
    #ipam_conn will be the actual API connection to our PHPIPAM frontend
    #py_section will be manual input for us eg. 'Python Testing'
    
    #phpipamsdk.SectionsApi is a class within a ton of methods for us to use (can be found in the readme for the library itself)
    apiSections = phpipamsdk.SectionsApi(phpipam=ipam_conn)

    #get_section_id will get the local ID of the section, an important value if we want to add/view/delete anything from that section
    sectionId = get_section_id(ipam=ipam_conn, name=py_section)

    #list_section_subnets will need the section ID (not a name, but a local ID number) and it will return every subnet within our section
    subnetlist = apiSections.list_section_subnets(section_id=sectionId)

    #Lets simply 
    if 'data' in subnetlist:
        for item in subnetlist['data']:
            print("ID: {0}\nSubnet: {1}\n\n".format(item['id'],item['subnet']))

#test
def create_a_subnet(ipam_conn=None, py_section=None, location=None, **kwargs):
    #We can allow optional parameters to be passed into this function (eg. we might not care about passing the description into a subnet on PHPIPAM)

    #SubnetsApi will be used, to call the methods such as 'add_subnet'
    #add_subnet method simply sends a payload to 'subnets/' (eg. https://ipaddress/subnets/
    apiSubnets = phpipamsdk.SubnetsApi(phpipam=ipam_conn)

    check = apiSubnets.add_subnet(
        subnet=kwargs['subnet'],
        mask=kwargs['mask'],
        description=kwargs['description'],
        section_id = get_section_id(ipam=ipam_conn, name=py_section),
        permissions=kwargs['permissions'],
        location_id=location
        )

    if 'id' in check:
        return check['id'] #Return the ID of the subnet... If we store this into a variable when we call the function, we don't need to later look for the local ID of the subnet...
    else:
        print("Something went wrong...")

def list_all_l2domains(ipam_conn=None):
    #Returns: id, name, description and sections
    apiL2Domains = phpipamsdk.L2DomainsApi(phpipam=ipam_conn)

    print(apiL2Domains.list_l2domains())

#Example {'id': '8', 'name': 'PYTHON-TEST2', 'description': None, 'sections': None}
def create_a_l2domain(ipam_conn=None, **kwargs):
    
    apiL2Domains = phpipamsdk.L2DomainsApi(phpipam=ipam_conn)

    check = apiL2Domains.add_l2domain(
        name=kwargs['name'],
        description=kwargs['description']
        )

    print(check)

    if 'id' in check:
        return check['id']
    else:
        print("Something went wrong...")

#Will list: 'id': '3', 'domainId': '1', 'name': 'VLAN100', 'number': '100', 'description': 'Test', 'editDate': None}], 'time': 0.003}
def list_all_vlans(ipam_conn=None):
    apiVlans = phpipamsdk.VlansApi(phpipam=ipam_conn)

    print(apiVlans.list_vlans())

def create_a_vlan(ipam_conn=None, l2domain=None, **kwargs):
    apiVlans = phpipamsdk.VlansApi(phpipam=ipam_conn)
    apiL2Domains = phpipamsdk.L2DomainsApi(phpipam=ipam_conn)

    local_id = '0'

    allL2Domains = apiL2Domains.list_l2domains()
    if 'data' in allL2Domains:
        for item in allL2Domains['data']:
            if l2domain in item['name']:
                local_id = item['id']

    check = apiVlans.add_vlan(
        name=kwargs['name'],
        number=kwargs['number'],
        domain_id=local_id
        )

    if 'id' in check:
        return check['id']
    else:
        print("Something went wrong...")

def netmikoGetVlanInfo(connection_details):

    _commandConfig = "show vlan brief | exc ----"

    try:
        _current_session = ConnectHandler(**connection_details)

        _current_session.enable()
        _getVlanInformation = _current_session.send_command(_commandConfig)

    except OSError as err:
        print("Error: {0}".format(err))

    ports = ['Fa','Gi','TenGi']

    index = 0

    vlan_list = []

    _vlans = _getVlanInformation.split('\n')
    _vlans = list(filter(None, _vlans))
    del _vlans[0] #Current index 0 is normally the heading eg. VLAN Status etc....

    for _vlan in _vlans:
        _vlan = _vlan.split()
        vlan_dict = {'vlanId' : _vlan[0], 'name' : _vlan[1]}
        vlan_list.append(vlan_dict)

    return vlan_list

if __name__ == "__main__":
    warnings.filterwarnings('ignore')

    #PhpIpamApi() is were the REST API magic happens, methods within this class handle the requests/tokens/authentication
    API = phpipamsdk.PhpIpamApi()

    #Simple a method within PhpIpamApi() class that checks if we will be using authentication, if so then it will send a http POST request which should return a token
    API.login()

    #call our function above to get all the subnets, section name is manual input, but we can do loads more with this function in a loop etc...
    #get_all_subnets(ipam_conn=API, py_section='Python Testing')

    #Permissions = SECTION Operators, SECTION Guests, something? something?

    #Store the function as a variable. When we print the result, it obviously creates the SUBNET itself but we have the local ID value that has been created...
    """
    subnetPrint = create_a_subnet(
        ipam_conn=API,
        py_section='Python Testing',
        subnet='10.0.3.0',
        mask='24',
        description='Created by automated Python Script',
        permissions='{"3":"1","2":"2"}'
        )
    print(subnetPrint)
    """

    #create_a_l2domain(ipam_conn=API, name='PY-DOMAIN-TEST', description='PYTHON VLAN L2 TEST')

    #list_all_vlans(ipam_conn=API)
    """
    index = 0
    vlan = 10

    while index <= 10:
        create_a_vlan(ipam_conn=API, name="VLAN" + str(vlan), number=vlan,l2domain='PY-DOMAIN-TEST')
        print("VLAN" + str(vlan) + " has been created...")
        vlan += 1
        index += 1
    """

    #create_a_vlan(ipam_conn=API, name='VLAN100', number='100',l2domain='PY-DOMAIN-TEST')

    for device in devices:
        
        print("Current device: {0}".format(device))
        ipAddr = device
        
        try:
            
            conn.update({'ip':   ipAddr})
            print(netmikoGetVlanInfo(conn))
            test = netmikoGetVlanInfo(conn)
            
            for vlan in test:
                print(vlan)
                create_a_vlan(ipam_conn=API, name=vlan['name'], number=vlan['vlanId'],l2domain='PY-DOMAIN-TEST')

        except OSError as err:
            print("Error: {0}".format(err))

    #Log out method will simply send a delete request 
    API.logout()
