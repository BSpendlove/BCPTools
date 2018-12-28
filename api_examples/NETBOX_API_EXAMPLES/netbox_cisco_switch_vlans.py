from pprint import pprint
from netbox import NetBox
from BCPTools.BCPTFunctions import bcp_create_session
from BCPTools.BCPTFunctions import bcp_show_vlans

#Cisco Switch connection details for Netmiko/BCPTools

conn = {
    'device_type': 'cisco_ios',
    'ip': '192.168.1.109',
    'username': 'hume',
    'password': 'cisco',
    'secret': 'cisco'
}

##---------------------- NETBOX API Login details ------------------------------##
myToken = 'mytoken123mytoken123mytoken123mytoken123'
api_login = NetBox(host='192.168.1.9', port=80, use_ssl=False, auth_token=myToken)
##------------------------------------------------------------------------------##

class bcp_vlan_functions(object):
	def create_vlan_group(self, netbox, name, slug, checkExists=True):
		if checkExists == True:

			vlan_group = netbox.ipam.get_vlan_groups(name=name)

			if not vlan_group:
				results = netbox.ipam.create_vlan_group(name=name, slug=slug)
				return results

			if name in vlan_group[0]['name']:
				print(name.lower() + " has already been configured as a VLAN Group... checkExist must be False if you would like to create a duplicate VLAN Group...")
				print("Local Database ID for vlan group: {0} is {1}\n".format(name,str(vlan_group[0]['id'])))

			else:
				results = netbox.ipam.create_vlan_group(name=name,slug=slug)
				return results

		else:
			print("Create vlan function without simple duplication...\n")
			results = netbox.ipam.create_vlan_group(name=name,slug=slug)
			return results

	def create_vlan(self, netbox, name, vlanid, groupname):
		vlan_check = netbox.ipam.get_vlans(name=name)
		vlangroups = self.get_vlan_group(netbox, groupname)
		site_id = self.get_vlan_group_site_id(netbox, groupname)

		if not vlangroups:
			print("VLAN Group {0} could not be found...".format(groupname))
			vlangroupid = None
			results = netbox.ipam.create_vlan(vlan_name=name,vid=vlanid,group=vlangroupid,site_id=None)
			return results

		else:
			vlangroupid = vlangroups[0]['id']

			if not vlan_check:
				results = netbox.ipam.create_vlan(vlan_name=name,vid=vlanid,group=vlangroupid,site=site_id)
				print("VLAN{0} ({1}) has been created...\n".format(vlanid, name))
				return results

			if name in vlan_check[0]['name']:
				if site_id in vlan_check[0]['site']:
					print("VLAN{0} exists in the Netbox Database and is already apart of VLAN Group {1}".format(vlanid, groupname))
				else:
					print("VLAN{0} exists in the Netbox database although there is no current VLAN belonging to the group {1}.. Configured for the VLAN Group {1}".format(name, groupname))
					netbox.ipam.create_vlan(vlan_name=name,vid=vlanid,group=vlangroupid,site=site_id)


	def get_vlan_group(self, netbox, vlanname):
		#Try to use either id or name to filter through VLAN groups, obviously ID is better if you have duplicate vlan group names, but with some common practice, you shouldn't configure 2 sites with the same 'VLAN group name'!!!
		return netbox.ipam.get_vlan_groups(name=vlanname)

	def save_vlans_to_netbox(self, netbox, groupname):
		session = bcp_create_session(conn)
		vlans = bcp_show_vlans(session)

		for vlan in vlans:
			self.create_vlan(netbox, vlan['name'], vlan['vlan_id'],groupname)

	def get_vlan_group_site_id(self, netbox, groupname):
		vlan_group = netbox.ipam.get_vlan_groups(name=groupname)
		return vlan_group[0]['site']['id']


#bcp_vlan_functions().create_vlan_group(api_login,"PYTHON-TEST-NETBOX","python-test-netbox")
print(bcp_vlan_functions().save_vlans_to_netbox(api_login, "Cafe Nero - London: Moorgate"))
#pprint(api_login.ipam.get_vlans(name="TEST-VLAN2"))
