"""

    ##########################################################################

    Ensure you fill out settings for the configuration in the python file:
    BCPTConfiguration.py

    ##########################################################################

    IMPORTANT NOTE:
    I've change the way this scripts as of Decemeber 2018. I felt like it was unnecessary to keep creating a new SSH session for
    each function that I call. So instead, I now prefer calling the bcp_create_session() in my main scripts (eg. in example scripts)
    so I can use the majority of my functions within a single SSH session.

    bcp_create_session is used to establish the SSH session by netmiko. Pass the netmiko connection details / dictionary into this if you want to use it...

    List of functions that can be used are detailed more on the readme at: https://github.com/BSpendlove/BCPTools

"""

from netmiko import ConnectHandler
import zipfile
import os
import time
import csv
import textfsm
from pprint import pprint
from datetime import datetime


def bcp_create_session(session_details):
    session = ConnectHandler(**session_details)
    session.enable()
    
    return(session)
    
def bcp_get_config(session, RemovePasswords=True):

    commandConfig = "show run"

    try:

        getRunningConfig = session.send_command(commandConfig)
        getHostname = session.find_prompt().replace('#','')
        
    except ValueError as err:
        print("Error: {0}".format(err))

    #Parse through configuration file and remove any password related commands
    #and also additional text we don't need...
    pwd_commands = ['enable password', 'enable secret', 'username', 'snmp-server community',
                    'tacacs-server key', 'radius-server key', 'key-string', 'ip ospf authentication-key']
    splitConfigFile = getRunningConfig.split('\n')

    index = 0

    if(RemovePasswords==True):
        for line in splitConfigFile:   
            for command in pwd_commands:
                if command in line:
                    splitConfigFile[index] = ("{0} <removed>".format(command))
            index += 1
            
    getRunningConfig = '\n'.join(splitConfigFile)
    
    try:
        if(os.path.exists('backups')):
            
            fileName = ("{0}_{1}".format(getHostname,datetime.now().strftime('%d-%m-%Y')))
            writeTextFile(os.path.join('backups', fileName), getRunningConfig)

        else:
            
            os.mkdir('backups')
            fileName = ("{0}_{1}".format(getHostname,datetime.now().strftime('%d-%m-%Y')))
            writeTextFile(os.path.join('backups', fileName), getRunningConfig)
            
    except OSError as err:
        print("OS Error: {0}".format(err))

def bcp_get_cdp_neighbors(session):

    command = 'show cdp neighbors detail'

    cdpresults = session.send_command(command)
    print(cdpresults)
    output = textfsm_extractor('cisco_ios_show_cdp_neighbors_detail.template', cdpresults)

    return output

def bcp_get_arp_table(session):

    command = 'show arp'

    arpresults = session.send_command(command)
    output = textfsm_extractor('cisco_ios_show_ip_arp.template', arpresults)

    return output

def bcp_get_mac_table(session):

    command = 'show mac address-table'

    macresults = session.send_command(command)
    output = textfsm_extractor('cisco_ios_show_mac-address-table.template', macresults)

    return output

def bcp_send_command(session, command):
    try:
        command_results = session.send_command(command)
        print(command_results)
        print("Completed...")

    except OSError as err:
        print("Error: {0}".format(err))

def bcp_get_vlans(session):
    vlans = session.send_command('show vlan')

def bcp_inventory_device_cisco(session, generatecsv=False, csvname="cisco_inventory.csv"):
	version = session.send_command('show version')
	inventory = session.send_command('show inventory')

	output_version = textfsm_extractor('cisco_ios_show_version.template',version)
	output_inventory = textfsm_extractor('cisco_ios_show_inventory.template',inventory)

	return output_version, output_inventory

def bcp_show_ip_int_brief(session):
    command = 'show ip interface brief'

    ipintbrief = session.send_command(command)

    output = textfsm_extractor('cisco_ios_show_ip_interface_brief.template', ipintbrief)
    return output

def bcp_show_interfaces(session):
    command = 'show interfaces'

    shinterfaces = session.send_command(command)

    output = textfsm_extractor('cisco_ios_show_interfaces.template',shinterfaces)
    return output

def bcp_show_vlans(session):
    command = 'show vlan'

    vlans = session.send_command(command)

    output = textfsm_extractor('cisco_ios_show_vlan.template', vlans)
    return output

def bcp_get_unused_interfaces(session):

    filterCommand = "sh int | i (down|output never|output [0-9]+[y]|output (1[2-9]|[2-9][0-9])[w])"

    try:

        getHostname = session.find_prompt().replace('#','')
        print("Hostname: ",getHostname)

        getInterfaceInformation = session.send_command(filterCommand)

    except OSError as err:
        print("Error: {0}".format(err))

    return(getInterfaceInformation)

#################################################
# This textfsm function was taken from NAPALM	#
# https://napalm-automation.net/		#
# https://github.com/napalm-automation/napalm   #
#################################################
def textfsm_extractor(template_name, raw_text):
    textfsm_data = list()
    fsm_handler = None

    template_directory = os.path.abspath(os.path.join(os.path.dirname(__file__),'textfsm_templates'))
    template_path = '{0}/{1}'.format(template_directory, template_name)

    with open(template_path) as f:
        fsm_handler = textfsm.TextFSM(f)

        for obj in fsm_handler.ParseText(raw_text):
            entry = {}
            for index, entry_value in enumerate(obj):
                entry[fsm_handler.header[index].lower()] = entry_value
            textfsm_data.append(entry)

        return textfsm_data

##############################################
#Simple write text file function
def writeTextFile(_name, _text):
    fileName = ("{0}.txt".format(_name))
    file = open(fileName,'w')

    file.write(_text)
    file.close()
##############################################

