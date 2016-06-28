# ARPANet Late 1960s - as per slide 2 lesson 2
'''
 +-------------------------------------------------------------------------+
 |                                                                         |
 |                                          +----------------+DART+------+ |
 |                                          |                    +       | |
 |             +-------------------------------------------+     |       + +
 |             |                            |              |     |       MAG+--+
 | +-----+UCB+--------+                     +              |     |             |
 | |       +   |      |                 +-+MICH+--------+  |     +             +
 | |       |   |      |                 |               |  +----+HARV          BBH+
 + +       +   |      +                 +               |           +   +------+  |
 SU       SRI+-+     UTAH+-----------+ILL        ++CMU  |           |   |         |
 +         +          +                +         | + +  |           |   |         |
 |         |          |            +---+         | | |  |           ++LC+         |
 |         |          |            |             | | |  |              +          |
 +         +          |            +             | | |  |              |          |
UCSB+----+UCLA        |           WH+------------+ | |  +------+BTL+---+          |
 +         +          |            +               | +           +                |
 |         |          |            |               |ARPA+--------+                |
 |         |          |            |               |                              |
 +         +          |            |               +------------------------------+
RAND+----+SDC+---------------------+
 +                    |
 +--------------------+

'''

topo = { 'SU' : ['UCSB', 'UCB', 'MAG'],
         'UCSB' : ['SU', 'UCLA', 'RAND'],
         'RAND' : ['UCSB', 'SDC', 'UTAH'],
         'UCB' : ['SU', 'SRI', 'UTAH'],
         'SRI' : ['UCB', 'UCLA', 'HARV'],
         'UCLA' : ['UCSB', 'SRI', 'SDC'],
         'SDC' : ['RAND', 'UCLA', 'WH'],
         'UTAH' : ['UCB', 'ILL', 'RAND'],
         'WH' : ['ILL', 'CMU', 'SDC'],
         'ILL' : ['UTAH', 'MICH', 'WH'],
         'MICH' : ['ILL', 'DART', 'BTL'],
         'CMU' : ['WH', 'BBH', 'ARPA'],
         'ARPA' : ['CMU', 'BTL'],
         'DART' : ['MICH', 'HARV', 'MAG'],
         'BTL' : ['MICH', 'ARPA', 'LC'],
         'HARV' : ['SRI', 'DART', 'LC'],
         'LC' : ['HARV', 'BTL', 'BBH'],
         'MAG' : ['DART', 'SU', 'BBH'],
         'BBH' : ['MAG', 'LC', 'CMU'] }