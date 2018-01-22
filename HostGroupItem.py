#!/usr/bin/env python
#
# Get item lastvalue for specified hostgroup from Zabbix checks
# Andy Fry <Andy.Fry@nec.com.au>
#
# Calls Zabbix API using pyzabbix (https://github.com/lukecyca/pyzabbix)
#

from pyzabbix import ZabbixAPI
import sys
import argparse

#Get Hostgroup and item key from command line
parser = argparse.ArgumentParser()
parser.add_argument('-g','--hostgroup', help="Zabbix Hostgroup Name", required=True)
parser.add_argument('-k','--itemkey', help="Item Key", required=True)
args = parser.parse_args()
hostgroup=args.hostgroup
itemkey=args.itemkey
username='USERNAME'
password='Password'
zabbix_server='Zabbix URL'


# Connect to Zabbix server
z=ZabbixAPI(server=zabbix_server)
z.session.verify=False
z.login(user=username, password=password)


# Get Hostgroup id
hostgroups=z.hostgroup.get(output="extend",
                           search={ "name": hostgroup },
                           sortfield='name',
                           sortorder='ASC')
if hostgroups:
    hostgroupid=hostgroups[0]['groupid']
else:
    sys.exit("Invalid Hostgroup")

#Get item Name for titles
items=z.item.get(output="extend",
                 search={ "key_": itemkey},
                 limit=1)
if items:
    itemname=items[0]['name']
else:
    sys.exit("Invalid item key")

output=["Hostname,", itemname]
print "".join(output)

# Get Hosts in the hostgroup
hosts=z.host.get(output="extend",
                 groupids=hostgroupid,
                 sortfield='name',
                 sortorder='ASC')
if hosts:
    # Get the lastvalue from each host
    for host in hosts:
        hostname = host['host']
        items=z.item.get(output="extend",
                         search={ "key_": itemkey},
                         host=hostname)
        if items:
            lastvalue=items[0]['lastvalue']
            output = [hostname, ",", lastvalue ]
            print "".join(output)
        else:
            sys.exit("No items found")
else:
    sys.exit("Host not found")
