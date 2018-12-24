# BCPTools
### Brandon's Cisco Project Tools

This is a personal project to learn python but also try to do something with python in terms of my job with network configuration and troubleshooting. I'm trying to write functions to return data from mainly Cisco devices but would like to try other devices in the future (it's just I currently work with Cisco the majority of the time)

I try to provide examples with my functions and will even try to provide real world examples when I've used them, some might be totally useless but others may be of help for other network engineers. I'm no expert at python, although I hope this project helps other people with looking into what you can do with python and network configuration etc..

## Installation
1. Create a directory, change directory and run:
```
git clone https://github.com/BSpendlove/BCPTools
```

2. Change directory into 'BCPTools' and run:
```
pip3 install -r requirements.txt
```
and then finally:
```
pip3 install .
```

Functions
=========

The majority of functions returns some data in json type format. I've used a function from the NAPALM library (https://github.com/napalm-automation/napalm) instead of using the inbuilt textfsm with Netmiko because I felt like it was limiting what I wanted to do. This is so I could use textfsm templates to structure the data from various 'show' commands on the devices. I would highly recommend using textfsm when working with large amounts of unstructured data like majority of 'show' commands on any vendors equipment.

<i>session</i> - This is normally the SSH session you can pass into the function (I normally use the bcp_create_session to pass into my other functions)

I also need to possibly arrange the below functions in alphabetical order... Not important right now since I keep adding to the list

bcp_create_session(<i>session_details</i>)
------------------------------------------
-Establishes SSH connection into global configuration mode using netmiko, you just need to pass the normal netmiko variables such as:
> device_type, ip, username, password, secret | etc....

bcp_get_config(<i>session</i>,<i>RemovePasswords=Boolean</i>)
-------------------------------------------------------------
-Creates directory 'backups' if it doesn't exist and then creates a backup, RemovePasswords is False by default but if True: it will remove any enable/username passwords, snmp communities, ospf authentication, tacacs+/radius secrets and key-string in a 'key chain'

bcp_get_cdp_neighbors(<i>session</i>)
-------------------------------------
-Returns JSON format of the following:
> capabilities, destination_host, local_port, management_ip, platform, remote_port, software_version

bcp_get_arp_table(<i>session</i>)
---------------------------------
-Returns JSON format of the following:
> address, age interface, mac, type

bcp_get_mac_table(<i>session</i>)
---------------------------------
-Returns JSON format of the following:
> destination_address, destination_port, type, vlan

bcp_send_command(<i>session</i>, <i>command</i>)
------------------------------------------------
-Not really useful, it's the same command as send_command() in netmiko but returns the output

bcp_inventory_device_cisco(<i>session</i>,<i>generatecsv=Boolean</i>,<i>csvname="mycsvname.csv"</i>)
----------------------------------------------------------------------------------------------------
-Returns JSON format of the following:
> config_register, hardware, hostname, reload_reason, rommon, running_image, serial, uptime, version, descr, name, pid, sn, vid

bcp_show_ip_int_brief(<i>session</i>)
-------------------------------------
-Returns JSON format of the following:
> interface, ipaddress, protocol, status

bcp_show_interfaces(<i>session</i>)
-----------------------------------
-Returns JSON format of the following:
> address, bandwidth, bia, delay, description, duplex, encapsulation, hardware_type, input_rate, interface, ip_address, link_status, mtu, output_rate, protocol_status, queue_strategy, speed

bcp_show_vlans(<i>session</i>)
------------------------------
-Returns JSON format of the following:
> interfaces, name, status, vlan_id

bcp_get_unused_interfaces(<i>session</i>)
-----------------------------------------
-Runs a include filter on the IOS command itself, a regex to filter out interfaces that haven't seen traffic in (or out) for more than 19 weeks...
