#!/usr/bin/python3


import time

from charm.toolbox.pairinggroup import PairingGroup, GT,ZR,G1,G2
from charm.toolbox.ecgroup import ECGroup
from charm.toolbox.eccurve import prime192v2, prime192v1
from charm.schemes.pkenc.pkenc_cs98 import CS98

# For AES
from charm.toolbox.pairinggroup import extract_key
from charm.toolbox.symcrypto import SymmetricCryptoAbstraction
from charm.core.math.pairing import hashPair as sha1
from charm.core.math.pairing import pair

# mg07a
from pre_mg07a_jet import PreGA


from ible import ible


    
###################################################

debug = True

# Message size := secparam / 8 (byte)
#group = PairingGroup('SS512', secparam=1024)
group = PairingGroup('SS512')
groupcs98 = ECGroup(prime192v2)
pkenc = CS98(groupcs98)

# Create pre cipher: __init__
pre = PreGA(group, pkenc)
# PRE SETUP
(msk, params) = pre.setup()
    
# Extarct the Sym key: bytes
#SymKey = extract_key(group.random(GT))

k = 'k' * 16  # 128 bits
SymKey = k.encode('utf-8')

# ID
ID = "Harry_Potter@gmail.com"

# Bytes message
msg = 'a' * 4096
m = msg.encode('utf-8')


f_log = open("ible_4096.log", "w")
localtime = time.asctime(time.localtime(time.time()))
# Trace File comments
f_log.write("#Created @ ")
f_log.write(str(localtime))
f_log.write("\n#SymE\tKeyIBE\tKeyIBD\tSymD (in milli-seconds)\n")

# Run counts
count = 1000


while count>=1:
    
    print("Run count = ", count)

    # Call IBLE algpr.
    ible(pre, ID, m, SymKey, msk, params, f_log)
    count -= 1

f_log.close()



    

