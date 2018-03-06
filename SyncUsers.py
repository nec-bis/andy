#!/usr/bin/env python
#
# Get Users from an existing zabbix server and synchronise to a secondary
# Andy Fry <Andy.Fry@nec.com.au>
#
# Calls Zabbix API using pyzabbix (https://github.com/lukecyca/pyzabbix)
#

from pyzabbix import ZabbixAPI, ZabbixAPIException
import sys
import argparse

#Added to ignore the SSL certificate warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

username='Admin'
password='Psbk^l&K'
primary_zabbix_server='https://pzab01/zabbix'
secondary_zabbix_server='https://szab01/zabbix'


# Connect to Primary Zabbix server
pz=ZabbixAPI(server=primary_zabbix_server)
pz.session.verify=False
pz.login(user=username, password=password)

sz=ZabbixAPI(server=secondary_zabbix_server)
sz.session.verify=False
sz.login(user=username, password=password)

# Get Users
for puser in pz.user.get(output="extend",
                  search={ "alias": [ "guest", "Admin" ] },
                  excludeSearch='on',
                  sortfield='userid',
                  sortorder='ASC'):
    print(puser['userid'],puser['name'],puser['surname'],puser['alias'])
    suser=sz.user.get(output="extend",
                  search={ "alias": puser['alias'] })
    if suser:
        print "No need to create this one"
    else:
        output=["User ", puser['alias'], " needs to be created"]
        print "".join(output)
        pusergrps=pz.usergroup.get(output="usergrpid",
                   userids=puser['userid'])
        if pusergrps:
            try:
                cuser=sz.user.create( alias=puser['alias'],
                              usrgrps=pusergrps,
                              passwd="Password123")
            except ZabbixAPIException as e:
                print(e)
