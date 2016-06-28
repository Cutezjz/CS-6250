############################################################################
# FILE: kparseall.sh                                                       #
# PATH: ~/cs6250-spring-2016/Project-2/_notes/testpart2/mine/kparseall.sh  #
############################################################################
 
#!/bin/bash
(
WDIR=/home/mininet/cs6250-spring-2016/Project-2/_notes/testpart2/mine/results
ALLOUT="${WDIR}/PARSED-ALL.txt"
(
for i in `find "${WDIR}" -type f -iname "nmap*txt" -not -iname "*PARSED*" | sort`; do
out=`dirname ${i}`/PARSED-`basename "${i}"`
echo "- parsing $i to $out"
python /home/mininet/cs6250-spring-2016/Project-2/_notes/testpart2/mine/kparsenmap.py -i "${i}" 2>&1 | tee "$out"
done
) 2>&1 | tee ${ALLOUT}
)