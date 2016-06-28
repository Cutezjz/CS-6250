# Marginally interesting topology
# 
# Ideally, this is a 4D cube.
# Here are the first three dimensions.
#  E--------F
#  |\      /|
#  | A----B |
#  | |    | |
#  | D----C |
#  |/      \|
#  H--------G
#

topo = { 'A' : ['B', 'D', 'E', 'L'],
         'B' : ['A', 'C', 'F', 'N'],
         'C' : ['B', 'D', 'G', 'P'],
         'D' : ['A', 'C', 'H', 'J'],
         'E' : ['A', 'F', 'H', 'K'],
         'F' : ['B', 'E', 'G', 'M'],
         'G' : ['C', 'F', 'H', 'O'],
         'H' : ['D', 'E', 'G', 'I'],
         'I' : ['H', 'J', 'K', 'O'],
         'J' : ['D', 'I', 'L', 'P'],
         'K' : ['E', 'I', 'L', 'M'],
         'L' : ['A', 'J', 'K', 'N'],
         'M' : ['F', 'K', 'N', 'O'],
         'N' : ['B', 'L', 'M', 'P'],
         'O' : ['G', 'I', 'M', 'P'],
         'P' : ['C', 'J', 'N', 'O'] }

# Here is the final round of my output, sorted alphabetically.
#-----
# A:A0,B1,C2,D1,E1,F2,G3,H2,I3,J2,K2,L1,M3,N2,O4,P3
# B:A1,B0,C1,D2,E2,F1,G2,H3,I4,J3,K3,L2,M2,N1,O3,P2
# C:A2,B1,C0,D1,E3,F2,G1,H2,I3,J2,K4,L3,M3,N2,O2,P1
# D:A1,B2,C1,D0,E2,F3,G2,H1,I2,J1,K3,L2,M4,N3,O3,P2
# E:A1,B2,C3,D2,E0,F1,G2,H1,I2,J3,K1,L2,M2,N3,O3,P4
# F:A2,B1,C2,D3,E1,F0,G1,H2,I3,J4,K2,L3,M1,N2,O2,P3
# G:A3,B2,C1,D2,E2,F1,G0,H1,I2,J3,K3,L4,M2,N3,O1,P2
# H:A2,B3,C2,D1,E1,F2,G1,H0,I1,J2,K2,L3,M3,N4,O2,P3
# I:A3,B4,C3,D2,E2,F3,G2,H1,I0,J1,K1,L2,M2,N3,O1,P2
# J:A2,B3,C2,D1,E3,F4,G3,H2,I1,J0,K2,L1,M3,N2,O2,P1
# K:A2,B3,C4,D3,E1,F2,G3,H2,I1,J2,K0,L1,M1,N2,O2,P3
# L:A1,B2,C3,D2,E2,F3,G4,H3,I2,J1,K1,L0,M2,N1,O3,P2
# M:A3,B2,C3,D4,E2,F1,G2,H3,I2,J3,K1,L2,M0,N1,O1,P2
# N:A2,B1,C2,D3,E3,F2,G3,H4,I3,J2,K2,L1,M1,N0,O2,P1
# O:A4,B3,C2,D3,E3,F2,G1,H2,I1,J2,K2,L3,M1,N2,O0,P1
# P:A3,B2,C1,D2,E4,F3,G2,H3,I2,J1,K3,L2,M2,N1,O1,P0
#
#Sorting any row by distance.
#-----
# A:A0,B1,D1,E1,L1,C2,F2,H2,J2,K2,N2,G3,I3,M3,P3,O4
# 1 at 0 -- 4 choose 0 -- 1 way  to find an object at dist 0 (using 0 dimen)
# 4 at 1 -- 4 choose 1 -- 4 ways to find an object at dist 1 (using 1 dimen)
# 6 at 2 -- 4 choose 2 -- 6 ways to find an object at dist 2 (using 2 dimen)
# 4 at 3 -- 4 choose 3 -- 4 ways to find an object at dist 3 (using 3 dimen)
# 1 at 4 -- 4 choose 4 -- 1 way  to find an object at dist 4 (using 4 dimen)
#
# Pascal's triangle.
#            1
#         1  -  1
#       1 -  2  - 1
#     1 - 3  -  3 - 1
#   1 - 4  - 6 -  4 - 1   --- 4 dimensional cube network
# 1 - 5 - 10 - 10 - 5 - 1
#
# This turns out not be very interesting for Bellman-Ford because every
# node is first discovered at its shortest distance.
#

