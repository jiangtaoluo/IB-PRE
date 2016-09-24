#!/usr/bin/python3

# Procedures:
# C1 = IBE(m, ID1)
# rk12 = genRK(sk1, ID2)
# C2 = RE(C1, rk12)
# m = IBD(C2, sk2)

import time

from charm.toolbox.pairinggroup import PairingGroup, GT
from charm.toolbox.ecgroup import ECGroup
from charm.toolbox.eccurve import prime192v2
from charm.schemes.pkenc.pkenc_cs98 import CS98



# mg07a
from pre_mg07a_jet import PreGA

from fibre import fibre

#

group = PairingGroup('SS512', secparam=1024)
groupcs98 = ECGroup(prime192v2)

pkenc = CS98(groupcs98)
pre = PreGA(group, pkenc)


# PRE SETUP
(mk, params) = pre.setup()


#(public_key, secret_key) = pkenc.keygen()

# Generate secret key for ID1
ID1 = "Harry_Potter@gmail.com"
ID2 = "Jet_Luo@gmail.com"

# Bytes message
msg = 'a' * 4096
m = msg.encode('utf-8')

f_log = open("fibre_4096.log", "w")
localtime = time.asctime(time.localtime(time.time()))
# Trace File comments
f_log.write("#Created @ ")
f_log.write(str(localtime))
f_log.write("\n#GenRK\tIBE\tRE\tIBD (in milli-seconds)\n")


# Run counts
count = 1000


#m = group.random(GT)    
while count>=1:
    
    print("Run count = ", count)
    # Random message
 
    fibre(pre, ID1, ID2, m, mk, params, f_log)
    count -= 1

f_log.close()



    

