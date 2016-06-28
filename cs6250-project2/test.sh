# Project 2: Test Methods - nmap
ifconfig | grep inet > report
nmap -p T:1080,2000-2004,2999-3002 -n -sA 10.0.0.1 10.0.0.2 10.0.0.3 10.0.0.4 10.0.0.5 10.0.0.6 >> report
subl report