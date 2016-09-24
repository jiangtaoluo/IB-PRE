#!/usr/bin/python3
''' 
Process the log file to calculate avage of each column

Date: Sep 22, 2016
Name: Jiangtao Luo

'''

import sys
import re
from operator import add
from decimal import *

if len(sys.argv) != 3:
    print("Usage error: ./process.py inlogname outfilename")
    sys.exit()


num = 0
header = ""

with open(sys.argv[1]) as ifile:
    for line in ifile:
        if line[0] != '#':  # skip the comment line beginning with '#'
            #print(line)
            # Trim '\n'
            num += 1
            line = line.strip()
            # Split the line with '\t'
            record = re.split(r'\t+', line)
            # translate into float
            record = [float(x) for x in record]
            #print(record)
            
            if num == 1:
                Sum = Min = Max = record
            else:
                Sum = list(map(add, Sum, record))

                Min = [min(x) for x in list(zip(Min, record))]
                Max = [max(x) for x in list(zip(Max, record))]
        else:
            header += line
print(header)
print("Number of records: ", num)
print("Min = ", Min)
print("Max = ", Max)

#Calculate the average
# Remove the Max and Min, and then calculate the Avgx
Sum = [(x1-x2-x3) for x1, x2, x3 in zip(Sum, Max, Min)]
Avg = [float('%.4f' % (x/(num-2))) for x in Sum]
print("Avg = ", Avg)

fo = open(sys.argv[2], "w")
# borrow the log fileheader
fo.write(header)

for x in Avg:
    fo.write(str(x))
    fo.write("\t")


            

    
