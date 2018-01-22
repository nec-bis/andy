#!/usr/bin/env python
#
#Get item lastvalue for specified Host Group
#Andy Fry<andy.fry@nec.com.au>
#
#Usage:
#    HostGroupItem -g <hostgroup> -k <itemkey>
#
#Calls ZabbixAPI using pyzabbix (https://github.com/lukecyca/pyzabbix)

from pyzabbix import ZabbixAPI
import sys
import argparse

#Get Host Group and item key from command line arguments
