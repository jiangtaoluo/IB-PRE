#!/usr/bin/python3
'''# Test Half IB-RE scheme
 Procedures:
 C = SymE(m, k)
 rk12 = genRK(sk1, ID2)
 ck = IBE(k, ID1)
 ck2 = RE(ck, rk12)
 dk = IBD(ck2, sk2)
 dm = SymE(C, dk)
'''
import time

from charm.toolbox.pairinggroup import PairingGroup, GT
from charm.toolbox.ecgroup import ECGroup
from charm.toolbox.eccurve import prime192v2
from charm.schemes.pkenc.pkenc_cs98 import CS98



# mg07a
from pre_mg07a_jet import PreGA

from hibre import hibre

#

group = PairingGroup('SS512', secparam=1024)
groupcs98 = ECGroup(prime192v2)

pkenc = CS98(groupcs98)
pre = PreGA(group, pkenc)


# PRE SETUP
(mk, params) = pre.setup()

# Set the Sym key: bytes
k = 'k' * 16  # 128 bits
SymKey = k.encode('utf-8')


# Generate secret key for ID1
ID1 = "Harry_Potter@gmail.com"
ID2 = "Jet_Luo@gmail.com"

# Bytes message
msg = 'a' * 4096
m = msg.encode('utf-8')

f_log = open("hibre_4096.log", "w")
localtime = time.asctime(time.localtime(time.time()))

# Trace File comments
f_log.write("#Created @ ")
f_log.write(str(localtime))
f_log.write("\n#SymE\tGenRK\tKeyIBE\tKeyRE\tKeyIBD\tSymD (in milli-seconds)\n")

# Run counts
count = 1000

while count>=1:
    
    print("Run count = ", count)
    # Random message
 
    hibre(pre, ID1, ID2, m, SymKey, mk, params, f_log)
    count -= 1

f_log.close()



    

