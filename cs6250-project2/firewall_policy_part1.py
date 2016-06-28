#!/usr/bin/python
															
"Project 2 - This creates the firewall policy. "

from pyretic.lib.corelib import *
from pyretic.lib.std import *
from pyretic.lib.query import packets
from pyretic.core import packet

def make_firewall_policy(config):
    # TODO - This is where you need to write the functionality to create the
    # firewall. What is passed in is a list of rules that you must implement.
    #Rule number, srcmac, dstmac, srcip, dstip, srcport, dstport
	
	# # feel free to remove the following "print config" line once you no longer need it
	print config # for demonstration purposes only, so you can see the format of the config
	rules = []
	for entry in config:
		if(entry['dstport']!="*"):
			rule = match(dstport=int(entry['dstport']), ethtype=packet.IPV4, protocol=packet.TCP_PROTO)
		if(entry['srcport']!="*"):	
			rule = match(srcport=int(entry['srcport']), ethtype=packet.IPV4, protocol=packet.TCP_PROTO)

        rules.append(rule)
        pass

   	allowed = ~(union(rules))
   	return allowed
