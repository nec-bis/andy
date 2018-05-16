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

#Added to ignore the SSL certificate warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

username='Admin'
password='Psbk^l&K'
zabbix_server='https://127.0.0.1/zabbix'


# Connect to Zabbix server
z=ZabbixAPI(server=zabbix_server)
z.session.verify=False
z.login(user=username, password=password)

# Get Users
for user in z.user.get(output="extend",
#                  search={ "surname": 'Administrator', "alias": 'guest' },
                  search={ "alias": [ "guest", "Admin" ] },
                  excludeSearch='on',
                  sortfield='userid',
                  sortorder='ASC'):
    print(user['userid'],user['alias'])
    for usergrp in z.usergroup.get(output="extend",
                     userids=user['userid']):
        print(usergrp)
