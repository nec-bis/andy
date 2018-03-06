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
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#Get Hostgroup and item key from command line
#parser = argparse.ArgumentParser()
#parser.add_argument('-g','--hostgroup', help="Zabbix Hostgroup Name", required=True)
#parser.add_argument('-k','--itemkey', help="Item Key", required=True)
#args = parser.parse_args()
#hostgroup=args.hostgroup
#itemkey=args.itemkey
username='Admin'
password='Psbk^l&K'
zabbix_server='https://127.0.0.1/zabbix'


# Connect to Zabbix server
z=ZabbixAPI(server=zabbix_server)
z.session.verify=False
z.login(user=username, password=password)

# Get Users
for user in z.user.get(output="extend",
                  search={ "alias": 'Admin', "alias": 'guest' },
                  excludeSearch='on',
                  searchByAny='false',
                  sortfield='userid',
                  sortorder='ASC'):
#    print(user['userid'],user['autologin'],user['autologout'],user['lang'])
    print(user)
