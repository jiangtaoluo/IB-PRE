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

from charm.toolbox.symcrypto import SymmetricCryptoAbstraction

# mg07a
from pre_mg07a_jet import PreGA


# F_IBRE function 
# msg: the original message in bytes, e.g. b"Hello, world"
# ID1: Sender's ID
# ID2: receipt's ID
# k: symmetric key
def hibre(pre, ID1, ID2, msg, k, master_key, params, log_file):
    if type(msg) != bytes: raise "Message type error: msg should be bytes."
    # switch for display
    #debug = True
    debug = False

    if debug:
        print("\nThe original message is: \n", msg)
    
    # Generate IBE private keys for IDs
    sk1 = pre.keyGen(master_key, ID1)
 
    sk2 = pre.keyGen(master_key, ID2)

    # Generate the Sym Cipher initilized by k
    symCipher = SymmetricCryptoAbstraction(k)

    # Symmetric Encrypt the message: AES(CTR) default
    t1 = time.time()
    ct = symCipher.encrypt(msg)
    t2 = time.time()
    t_aes = (t2-t1)*1000
    log = '{0:.4f}'.format(t_aes)+"\t"

    # Generate Re-Key (1-->2), using sk1 and ID2
    t1 = time.time()
    rk = pre.rkGen(params, sk1, ID2)
    t2 = time.time()
    t_grk = (t2-t1)*1000

    log += '{0:.4f}'.format(t_grk) + "\t"
    
    # IBE the sym key using ID1: IBE1
    t1 = time.time()
    ck = pre.encrypt_jet(params, ID1, k)
    t2 = time.time()
    t_kibe = (t2-t1)*1000
 
    log += '{0:.4f}'.format(t_kibe) + "\t"

    # Re-encrypt using Re-Key
    t1 = time.time()
    ck2 = pre.reEncrypt_jet(params, rk, ck)
    t2 = time.time()
    t_kre = (t2-t1)*1000
    log += '{0:.4f}'.format(t_kre) + "\t"

    # IBD using sk2 to get sym key
    t1 = time.time()
    dk =pre.decrypt_jet(params, sk2, ck2)
    t2 = time.time()
    t_kibd = (t2-t1)*1000
    log += '{0:.4f}'.format(t_kibd) + "\t"

    # Sym decrypt using the IBD output
    # Generate sym cipher using the output key
    decipher = SymmetricCryptoAbstraction(dk)

    t1 = time.time()
    dmsg = decipher.decrypt(ct)
    t2 = time.time()
    t_aes2 = (t2-t1)*1000
    log += '{0:.4f}'.format(t_aes2)+"\n"

    if debug:
        print("\nThe decrypted message is:\n", dmsg)
    assert dmsg == msg , 'o: =>%s\nm: =>%s' % (msg, dmsg)
    
    log_file.write(log)
 



    

