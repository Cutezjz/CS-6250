#Author Pico Geyer
#Contributors:
# Robert Moe

import time
import re
import random
import os.path

from mininet.topo import Topo
from mininet.net  import Mininet
from mininet.node import CPULimitedHost, RemoteController
from mininet.util import custom
from mininet.link import TCLink
from mininet.cli  import CLI

class FWTopo(Topo):
    ''' Creates the following topoplogy:
     e1   e2   e3
     |    |    |
      \   |   /
      firwall (s1)
      /   |   \
     |    |    |
    w1    w2   w3
    '''
    def __init__(self, cpu=.1, bw=10, delay=None, **params):
        super(FWTopo,self).__init__()

        # Host in link configuration
        hconfig = {'cpu': cpu}
        lconfig = {'bw': bw, 'delay': delay}

        # Create the firewall switch
        s1 = self.addSwitch('s1')

        # Create East hosts and links)
        e1 = self.addHost('e1', **hconfig)
        e2 = self.addHost('e2', **hconfig)
        e3 = self.addHost('e3', **hconfig)
        self.addLink(s1, e1, port1=1, port2=1, **lconfig)
        self.addLink(s1, e2, port1=2, port2=1, **lconfig)
        self.addLink(s1, e3, port1=3, port2=1, **lconfig)

        # Create West hosts and links)
        w1 = self.addHost('w1', **hconfig)
        w2 = self.addHost('w2', **hconfig)
        w3 = self.addHost('w3', **hconfig)
        self.addLink(s1, w1, port1=4, port2=1, **lconfig)
        self.addLink(s1, w2, port1=5, port2=1, **lconfig)
        self.addLink(s1, w3, port1=6, port2=1, **lconfig)


class SetupError(Exception): pass
class TestFailure(Exception): pass

required_hosts = ['e1', 'e2', 'e3', 'w1', 'w2', 'w3']
tools_path=''
total_test_cases = 0
num_test_passed = 0
num_test_failed = 0

#Implementation of tests.
#Each test should clean up after itself so as not to affect the other tests

def block_east_west_port_1080(mn):
    global total_test_cases
    global num_test_passed
    global num_test_failed

    print "***************************************************************************************"
    print "TEST 1: 'Block all traffic in both directions between the East and West on port 1080'"
    print "***************************************************************************************"
    failed = False

    port = 1080

    east = ['e1', 'e2', 'e3']
    west = ['w1', 'w2', 'w3']

    # Test East to West
    for e in east:
        for w in west:
            total_test_cases += 1
            if testconnection(mn, w, e, port):
                num_test_failed += 1
                failed = True
                print 'FAIL: Connection established from client ({}) to server ({}) on port ({})'.format(e, w, port)
            else:
                num_test_passed += 1
                print 'PASS: Connection refused from client ({}) to server ({}) on port ({})'.format(e, w, port)

    # Test West to East
    for w in west:
        for e in east:
            total_test_cases += 1
            if testconnection(mn, e, w, port):
                num_test_failed += 1
                failed = True
                print 'FAIL: Connection established from client ({}) to server ({}) on port ({})'.format(w, e, port)
            else:
                num_test_passed += 1
                print 'PASS: Connection refused from client ({}) to server ({}) on port ({})'.format(w, e, port)

    if failed:
        raise TestFailure("FAILED: 'Block all traffic in both directions between the East and West on port 1080'")
    else:
        print "PASSED: 'Block all traffic in both directions between the East and West on port 1080'"

def allow_traffic_within_east_west(mn):
    global total_test_cases
    global num_test_passed
    global num_test_failed

    print "***********************************************************************************"
    print "TEST 2: 'Allow all traffic within the East or West sites to port 1080'"
    print "***********************************************************************************"
    failed = False

    #port = 1080
    port = 1080

    east = ['e1', 'e2', 'e3']
    west = ['w1', 'w2', 'w3']

    # Test East Container
    for e in east:
        for e1 in east:
            if e != e1:
                total_test_cases += 1
                if testconnection(mn, e, e1, port):
                    num_test_passed += 1
                    print 'PASS: Connection established from client ({}) to server ({}) on port ({})'.format(e1, e, port)
                else:
                    num_test_failed += 1
                    failed = True
                    print 'FAIL: Connection could not be established from client ({}) to server ({}) on port ({})'.format(e1, e, port)

    # Test West Container
    for w in west:
        for w1 in west:
            if w != w1:
                total_test_cases += 1
                if testconnection(mn, w, w1, port):
                    num_test_passed += 1
                    print 'PASS: Connection established from client ({}) to server ({}) on port ({})'.format(w1, w, port)
                else:
                    num_test_failed += 1
                    failed = True
                    print 'FAIL: Connection could not be established from client ({}) to server ({}) on port ({})'.format(w1, w, port)

    if failed:
        raise TestFailure("FAILED: 'Allow all traffic within the East or West sites to port 1080'")
    else:
        print "PASSED: 'Allow all traffic within the East or West sites to port 1080'"

def block_e1_to_w1_completely(mn):
    global total_test_cases
    global num_test_passed
    global num_test_failed

    print "***********************************************************************************"
    print "TEST 3: 'Block e1 from communicating with w1 completely in both directions'"
    print "***********************************************************************************"

    # Pick 20 random numbers between port 1024 and 10000
    ports = random.sample(xrange(1024, 10000), 20)

    failed = False

    # Test East To West
    for port in ports:
        total_test_cases += 1
        if testconnection(mn, 'w1', 'e1', port):
            num_test_failed += 1
            failed = True
            print 'FAIL: Connection established from client ({}) to server ({}) on port ({})'.format('e1', 'w1', port)
        else:
            num_test_passed += 1
            print 'PASS: Connection refused from client ({}) to server ({}) on port ({})'.format('e1', 'w1', port)

    # Test West To East
    for port in ports:
        total_test_cases += 1
        if testconnection(mn, 'e1', 'w1', port):
            num_test_failed += 1
            failed = True
            print 'FAIL: Connection established from client ({}) to server ({}) on port ({})'.format('w1', 'e1', port)
        else:
            num_test_passed += 1
            print 'PASS: Connection refused from client ({}) to server ({}) on port ({})'.format('w1', 'e1', port)

    if failed:
        raise TestFailure("FAILED 'Block e1 from communicating with w1 completely in both directions'")
    else:
        print "PASSED: 'Block e1 from communicating with w1 completely in both directions'"

def block_e2_to_w2_over_2000(mn):
    global total_test_cases
    global num_test_passed
    global num_test_failed

    print "***********************************************************************************"
    print "TEST 4: 'Block e2 from communicating with w2 over ports 2000-2004 in both directions'"
    print "***********************************************************************************"

    failed = False

    ports = list(xrange(2000, 2005))

    # Test East To West
    for port in ports:
        total_test_cases += 1
        if testconnection(mn, 'w2', 'e2', port):
            num_test_failed += 1
            failed = True
            print 'FAIL: Connection established from client ({}) to server ({}) on port ({})'.format('e2', 'w2', port)
        else:
            num_test_passed += 1
            print 'PASS: Connection refused from client ({}) to server ({}) on port ({})'.format('e2', 'w2', port)

    # Test West To East
    for port in ports:
        total_test_cases += 1
        if testconnection(mn, 'e2', 'w2', port):
            num_test_failed += 1
            failed = True
            print 'FAIL: Connection established from client ({}) to server ({}) on port ({})'.format('w2', 'e2', port)
        else:
            num_test_passed += 1
            print 'PASS: Connection refused from client ({}) to server ({}) on port ({})'.format('w2', 'e2', port)

    if failed:
        raise TestFailure("FAILED 'Block e2 from communicating with w2 over ports 2000-2004 in both directions'")
    else:
        print "PASSED: 'Block e2 from communicating with w2 over ports 2000-2004 in both directions'"



def block_e3_to_w3_over_3000(mn):
    global total_test_cases
    global num_test_passed
    global num_test_failed

    print "***********************************************************************************"
    print "TEST 5: 'Block e3 from communicating with w3 over ports 3000-3002"
    print "         but allow w3 to communicate with e3 over those same ports'"
    print "***********************************************************************************"

    failed = False

    ports = list(xrange(3000, 3003))

    # Test East To West
    for port in ports:
        total_test_cases += 1
        if testconnection(mn, 'w3', 'e3', port):
            num_test_failed += 1
            failed = True
            print 'FAIL: Connection established from client ({}) to server ({}) on port ({})'.format('e3', 'w3', port)
        else:
            num_test_passed += 1
            print 'PASS: Connection refused from client ({}) to server ({}) on port ({})'.format('e3', 'w3', port)

    # Test West To East
    for port in ports:
        total_test_cases += 1
        if testconnection(mn, 'e3', 'w3', port):
            num_test_passed += 1
            print 'PASS: Connection established from client ({}) to server ({}) on port ({})'.format('w3', 'e3', port)
        else:
            num_test_failed += 1
            failed = True
            print 'FAIL: Connection refused from client ({}) to server ({}) on port ({})'.format('w3', 'e3', port)

    if failed:
        raise TestFailure("FAILED 'Block e3 from communicating with w3 over ports 3000-3002'")
    else:
        print "PASSED: 'Block e3 from communicating with w3 over ports 3000-3002'"

def testconnection(mn, server, client, port):

    client_host = mn.get(client)
    server_host = mn.get(server)

    client_IP = client_host.IP()
    server_IP = server_host.IP()

    print 'Starting server ({}) on {}:{}'.format(server, server_IP, port)
    server_host.sendCmd('python {} {} {}'.format(
        os.path.join(tools_path, 'test-server.py'),
        server_IP,
        int(port)),
        printPid=True)
    time.sleep(1)

    print 'Starting client ({}) connecting to {}:{}'.format(client, server_IP, port)
    client_host.sendCmd('python {} {} {}'.format(
        os.path.join(tools_path, 'test-client.py'),
        server_IP,
        int(port)),
        printPid=True)
    time.sleep(1)

    client_host.sendInt()
    server_host.sendInt()

    client_data = client_host.monitor()
    server_data = server_host.monitor()

    client_host.waiting = server_host.waiting = False

    if 'received' in client_data:
        return True
    return False

def check_hosts(mn):
    missing_host = False
    for r in required_hosts:
        try:
            mn.get(r)
        except KeyError:
            print 'Required host {} seems to be missing from the topology'.format(r)
            missing_host = True
    if missing_host:
        raise SetupError("Missing hosts")

def check_setup():
    #Make sure we can find our tools
    global tools_path
    #first check for tools in current dir
    if os.path.exists('test-client.py'):
        tools_path=os.path.abspath('.')
    elif os.path.exists('../test-client.py'):
        tools_path=os.path.abspath('..')
    else:
        raise SetupError('Can\'t find testing tools')

def run_tests(mn):
    #list of tests to run, edit as needed
    tests = ['block_east_west_port_1080',
             'allow_traffic_within_east_west',
             'block_e1_to_w1_completely',
             'block_e2_to_w2_over_2000',
             'block_e3_to_w3_over_3000']
    #first do a sanity check
    check_hosts(mn)
    check_setup()
    mn.pingAll()
    for t in tests:
        to = globals()[t]
        try:
            to(mn)
        except KeyboardInterrupt:
            raise
        except Exception as e:
            print str(e)

def main():
    print "Starting topology"
    topo = FWTopo()
    net = Mininet(topo=topo, link=TCLink, controller=RemoteController, autoSetMacs=True)

    net.start()

    run_tests(net)
    print "***************************** SUMMARY *********************************************"
    print 'Total test cases: {}'.format(total_test_cases)
    print 'PASSED: {}/{} '.format(num_test_passed, total_test_cases)
    print 'FAILED: {}/{}'.format(num_test_failed, total_test_cases)
    print "***********************************************************************************"

if __name__ == '__main__':
    main()