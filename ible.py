#!/usr/bin/python3

# Procedures:
# (ID, sk_ID) = GenKey
# C = AES(m, k)
# ck = IBE(k, ID)
# ......
# k = IBD(ck, sk_ID)
# m = AES(C, k)

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


# IBPRE function
# pre: IB-PRE cipher generated outside
# msg: the original message in bytes, e.g. b"Hello, world"
# ID: Receiver's ID
# k: symmetric key for message
def ible(pre, ID, msg, k, master_key, params, log_file):
 
    if type(msg) != bytes: raise "Message type error: msg should be bytes."
  
    # switch for display
    #debug = True
    debug = False

    if debug:
        print("\nThe original message is: \n", msg)
    
    # Generate the Sym Cipher initilized by k
    symCipher = SymmetricCryptoAbstraction(k)

    # Symmetric Encrypt: AES(CTR) default
    t1 = time.time()
    ct = symCipher.encrypt(msg)
    t2 = time.time()
    t_aes = (t2-t1)*1000
    log = '{0:.4f}'.format(t_aes)+"\t"
    
    
    # Generate private keys for ID
    sk1 = pre.keyGen(master_key, ID)
  
    # Encrypt 'Sym k' using ID
    t1 = time.time()
    ck = pre.encrypt_jet(params, ID, k)
    t2 = time.time()
    t_ibe = (t2-t1)*1000
    log += '{0:.4f}'.format(t_ibe) + "\t"

    # decryption using sk1
    t1 = time.time()
    dk =pre.decrypt_jet(params, sk1, ck)
    t2 = time.time()
    t_ibd = (t2-t1)*1000
    log += '{0:.4f}'.format(t_ibd) + "\t"

    if debug:
        print("\nThe decrypted key is:\n", dk)


    # Transmit dk and ct to the receipt
    # ........
    
    # Sym decrypt using the IBD output
    decipher = SymmetricCryptoAbstraction(dk)

    t1 = time.time()
    dmsg = decipher.decrypt(ct)
    t2 = time.time()
    t_aes2 = (t2-t1)*1000
    log += '{0:.4f}'.format(t_aes2)+"\n"

    if debug:
        print("\nThe decrypted message is:\n", dmsg)
    assert dmsg == msg , 'o: =>%s\nm: =>%s' % (msg, dmsg)
    # output log
    log_file.write(log)


    

