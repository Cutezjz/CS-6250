############################################################################
# FILE: kparsenmap.py                                                      #
# PATH: ~/cs6250-spring-2016/Project-2/_notes/testpart2/mine/kparsenmap.py #
############################################################################
 
#!/usr/bin/env python
#Author:Bill Turczyn
#Date: 2016/02/03 20:45:50
#Desc: Parse the nmap Grepable output to produce a table
 
import sys
import os
import argparse
import re
import pprint
 
if __name__ == "__main__":
    #you can add hosts to this table if your topology contains more
    host_table_lookup = { '10.0.0.1': 'e1',
                   '10.0.0.2': 'e2',
                   '10.0.0.3': 'e3',
                   '10.0.0.4': 'w1',
                   '10.0.0.5': 'w2',
                   '10.0.0.6': 'w3',}
    hosts_results = {}
    pp = pprint.PrettyPrinter(depth=6)
    port_indicies = {'PORT':0, 'STATE':1, 'PROTOCOL':3, 'SERVICE' :4}
    #Host: 10.0.0.2 ()  Ports: 1080/unfiltered/tcp//socks///
    status_line=re.compile('status:',re.IGNORECASE)
    port_line=re.compile('ports:',re.IGNORECASE)
    replace_extra_white_space=re.compile('\s{1,}')
    replace_extra_strokes=re.compile('\/{2,}')
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--infile',type=str, required=True)
    args = parser.parse_args()
    the_file = args.infile
    try:
        print "Parsing %s file..." % (the_file)
        hostname = the_file.split('_')[-1].replace('.txt','')
        fd = open(the_file,'r')
        for line in fd.readlines():
             line = replace_extra_white_space.sub('',line)
             line = replace_extra_strokes.sub('',line)
             if status_line.search(line):
                 the_host=line[0:line.find('(')].split(':')[1]
                 if host_table_lookup.has_key(the_host):
                     the_host="%s <--> %s" % (hostname,host_table_lookup[the_host])
                 else:
                     the_host="%s <--> %s" % (hostname,the_host)
 
                 hosts_results.setdefault(the_host, {'status':line.split(':')[2]})
             if port_line.search(line):
                 the_host=line.split(':')[1]
                 the_host=the_host[0:the_host.find('(')]
                 if host_table_lookup.has_key(the_host):
                     the_host="%s <--> %s" % (hostname,host_table_lookup[the_host])
                 else:
                     the_host="%s <--> %s" % (hostname,the_host)
                 for port in line.split(':')[-1].split(","):
                     port_info = port.split('/')
                     hosts_results[the_host].update({port_info[port_indicies['PORT']] : port_info[port_indicies['STATE']]})
        pp.pprint( hosts_results)
    except Exception,e:
        print "ERROR (%s)" % (e)
