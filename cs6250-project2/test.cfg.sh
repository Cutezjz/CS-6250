# Rule number, srcmac, dstmac, srcip, dstip, srcport, dstport
# Rule number is incremented each time - mostly for debug purposes
# * is wildcard. The following rule would block any traffic going to port 80.
# 1, *, *, *, *, *, 80
# Comments are on their own line


# Block all traffic in both directions between the East (e1, e2, e3) and West (w1, w2, w3) on port 1080
# Allow all traffic (that is, don't block) within the East or West sides to port 1080. That is e1 should be able to connect to e2, and w1 should be #able to connect to w2
	#block traffic from e1, e2, e3 to w1, w2 ,w3 
#1,*, *, 10.0.0.1, 10.0.0.6, *, 1080
1, 00:00:00:00:00:01,*,*,10.0.0.6, *, 1080
2,*, *, 10.0.0.1, 10.0.0.5, *, 1080
3,*, *, 10.0.0.1, 10.0.0.4, *, *
4,*, *, 10.0.0.2, 10.0.0.6, *, 1080
5,*, *, 10.0.0.2, 10.0.0.5, *, 1080
6,*, *, 10.0.0.2, 10.0.0.4, *, 1080
7,*, *, 10.0.0.3, 10.0.0.6, *, 1080
8,*, *, 10.0.0.3, 10.0.0.5, *, 1080
9,*, *, 10.0.0.3, 10.0.0.4, *, 1080

	#block traffic from w1,w2,w3 to e1,e2,e3

10,*, *, 10.0.0.4, 10.0.0.1, *, *
11,*, *, 10.0.0.4, 10.0.0.2, *, 1080
12,*, *, 10.0.0.4, 10.0.0.3, *, 1080
13,*, *, 10.0.0.5, 10.0.0.1, *, 1080
14,*, *, 10.0.0.5, 10.0.0.2, *, 1080
15,*, *, 10.0.0.5, 10.0.0.3, *, 1080
#16,*, *, 10.0.0.6, 10.0.0.1, *, 1080
16,00:00:00:00:00:06, *, *, 10.0.0.1, *, 1080
17,*, *, 10.0.0.6, 10.0.0.2, *, 1080
18,*, *, 10.0.0.6, 10.0.0.3, *, 1080

#Block e2 from communicating with w2 over ports 2000-2004 in both directions
19,*, *, 10.0.0.2, 10.0.0.5, *, 2000
20,*, *, 10.0.0.2, 10.0.0.5, *, 2001
21,*, *, 10.0.0.2, 10.0.0.5, *, 2002
22,*, *, 10.0.0.2, 10.0.0.5, *, 2003
23,*, *, 10.0.0.2, 10.0.0.5, *, 2004

24,*, *, 10.0.0.5, 10.0.0.2, *, 2000
25,*, *, 10.0.0.5, 10.0.0.2, *, 2001
26,*, *, 10.0.0.5, 10.0.0.2, *, 2002
27,*, *, 10.0.0.5, 10.0.0.2, *, 2003
28,*, *, 10.0.0.5, 10.0.0.2, *, 2004

#Block e3 from communicating with w3 over ports 3000-3002, but allow w3 to communicate with e3 over those same ports
29,*, *, 10.0.0.3, 10.0.0.6, *, 3000
30,*, *, 10.0.0.3, 10.0.0.6, *, 3001
31,*, *, 10.0.0.3, 10.0.0.6, *, 3002




#Block e1 from communicating with w1 completely in both directions
#Block e2 from communicating with w2 over ports 2000-2004 in both directions
#Block e3 from communicating with w3 over ports 3000-3002, but allow w3 to communicate with e3 over those same ports