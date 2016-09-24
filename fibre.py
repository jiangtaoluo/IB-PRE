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


# F_IBRE function 
# msg: the original message in bytes, e.g. b"Hello, world"
# ID1: Sender's ID
# ID2: receipt's ID
def fibre(pre, ID1, ID2, msg, master_key, params, log_file):
    # # Procedures:
    # C1 = IBE(m, ID1)
    # rk12 = genRK(sk1, ID2)
    # C2 = RE(C1, rk12)
    # m = IBD(C2, sk2)
    # wirite benchmark in log_file

    if type(msg) != bytes: raise "Message type error: msg should be bytes."
    # switch for display
    #debug = True
    debug = False

    if debug:
        print("\nThe original message is: \n", msg)
    
    # Generate IBE private keys for IDs
    sk1 = pre.keyGen(master_key, ID1)
 
    sk2 = pre.keyGen(master_key, ID2)
    
   # Generate Re-Key (1-->2), using sk1 and ID2
    t1 = time.time()
    rk = pre.rkGen(params, sk1, ID2)
    t2 = time.time()
    t_grk = (t2-t1)*1000

    log = '{0:.4f}'.format(t_grk) + "\t"
    
    # Encryption using ID1: IBE1
    t1 = time.time()
    C1 = pre.encrypt_jet(params, ID1, msg)
    t2 = time.time()
    t_enc = (t2-t1)*1000
    if debug:
        print("IBE ciphered Text is: ", C1)

    log += '{0:.4f}'.format(t_enc) + "\t"

    # Re-encrypt using Re-Key
    t1 = time.time()
    rc = pre.reEncrypt_jet(params, rk, C1)
    t2 = time.time()
    t_re = (t2-t1)*1000
    log += '{0:.4f}'.format(t_re) + "\t"

    # decryption using sk2
    t1 = time.time()
    m2 =pre.decrypt_jet(params, sk2, rc)
    t2 = time.time()
    t_de = (t2-t1)*1000
    log += '{0:.4f}'.format(t_de) + "\n"

    if debug:
        print("\nThe decrypted message is:\n", m2)

    log_file.write(log)
 



    

