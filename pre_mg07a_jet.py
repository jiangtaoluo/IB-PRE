'''
Identity-Based Proxy Re-Encryption

| From: "M. Green, G. Ateniese Identity-Based Proxy Re-Encryption", Section 4.1.
| Published in: Applied Cryptography and Network Security. Springer Berlin/Heidelberg, 2007
| Available from: http://link.springer.com/chapter/10.1007%2F978-3-540-72738-5_19

* type:           proxy encryption (identity-based)
* setting:        bilinear groups (symmetric)

:Authors:    N. Fotiou
:Date:       7/2016

: Extended by Jiangtao Luo (Luojt2008@gmail.com) to support bytes encryption, 
: Date: 9/2016
'''


from charm.toolbox.pairinggroup import pc_element,ZR,G1,G2,GT,pair
from charm.core.math.integer import integer,bitsize, int2Bytes, randomBits
from charm.toolbox.hash_module import Hash
from charm.core.engine.util import objectToBytes, bytesToObject
from charm.adapters.pkenc_adapt_hybrid import HybridEnc

#Jet
from charm.toolbox.symcrypto import AuthenticatedCryptoAbstraction
from charm.core.math.pairing import hashPair as sha1


#debug = True
debug = False
class PreGA:
    """
	>>>  from charm.toolbox.pairinggroup import PairingGroup,GT
	>>>  from charm.core.engine.util import objectToBytes,bytesToObject
	>>>  from charm.schemes.pkenc.pkenc_cs98 import CS98
	>>>  from charm.toolbox.ecgroup import ECGroup
	>>>  from charm.toolbox.eccurve import prime192v2
	>>>  group = PairingGroup('SS512', secparam=1024)
	>>>  groupcs98 = ECGroup(prime192v2) 
	>>>  pkenc = CS98(groupcs98)
	>>>  pre = PreGA(group,pkenc)
	>>>  ID1 = "nikos fotiou"
	>>>  msg  =  group.random(GT) 
	>>>  (master_secret_key, params) = pre.setup()
	>>>  (public_key, secret_key) = pkenc.keygen()
	>>>  id1_secret_key = pre.keyGen(master_secret_key, ID1)
	>>>  ciphertext = pre.encrypt(params, ID1, msg);
	>>>  re_encryption_key = pre.rkGenPKenc(params,id1_secret_key, public_key)
	>>>  ciphertext2 = pre.reEncryptPKenc(params, re_encryption_key, ciphertext)
	>>>  pre.decryptPKenc(params,public_key, secret_key, ciphertext2)
    """
    def __init__(self, groupObj, pkencObj = None):
        global group,h, pkenc
        group = groupObj
        h = Hash('sha1', group)
        if pkencObj != None:
            pkenc = HybridEnc(pkencObj)
        
    def setup(self):
        # Note: different type: ZR vs G1
        s = group.random(ZR) # a big integer
        g =  group.random(G1) # a pair
        msk = { 's':s }
        params = { 'g':g, 'g_s':g**s}
        if(debug):
            print("Public parameters...")
            group.debug(params)
            print("Master secret key...")
            group.debug(msk)
        return (msk, params)

    def keyGen(self, msk, ID):
        k = group.hash(ID,G1) ** msk['s']
        skid = { 'skid':k }        
        if(debug):
            print("Key for id => '%s'" % ID)
            group.debug(skid)
        return skid

    def encrypt(self, params, ID, m):
        #r = h.group.random(ZR)   # Jet, Sep 16, 2016
        r = group.random(ZR) # a large integer
        C1 = params['g'] ** r 
        C2 = m *(pair(params['g_s'],group.hash(ID, G1)) ** r)
        # Generate the ciphertext: a Dictionary
        ciphertext = {'C1':C1, 'C2':C2}           
        if(debug):
            print('m=>')
            print(m)
            print('ciphertext => ')
            print(ciphertext)
        return ciphertext
        
    def decrypt(self, params, skid, cid):
        if len(cid) == 2: # first level ciphertext # Jet: Normal IBE
            m = cid['C2']/pair(cid['C1'],skid['skid'])
        if len(cid) == 4: # second level ciphertext
            #Jet: decrypt the re-encrypted content
            
            x = self.decrypt(params, skid,{'C1':cid['C3'], 'C2':cid['C4']})           
            m = cid['C2']/pair(cid['C1'],group.hash(x,G1))            
        if(debug):
            print('\nDecrypting...')
            print('m=>')
            print(m)
        return m
    
    def rkGen(self, params, skid, ID2):
        X = group.random(GT)
        enc = self.encrypt(params, ID2, X) 
        rk = {'R1':enc['C1'], 'R2':enc['C2'], 'R3':(1/(skid['skid']))*group.hash(X,G1)}
        if(debug):
            print("\nRe-encryption key  =>" )
            print(rk)
        return  rk
        
    def reEncrypt(self, params, rk, cid):
        ciphertext = {'C1':cid['C1'], 'C2':cid['C2']*pair(cid['C1'],rk['R3']), 'C3':rk['R1'], 'C4':rk['R2']}
        if(debug):
            print('ciphertext => ')
            print(ciphertext)
        return ciphertext
    
    def rkGenPKenc(self, params, skid, public_key):
        X = group.random(GT)
        Xbytes = objectToBytes( X, group)
        enc = pkenc.encrypt(public_key, Xbytes)
        rk = {'R1':enc,  'R2':(1/(skid['skid']))*group.hash(X,G1)}
        if(debug):
            print("\nRe-encryption key  =>" )
            print(rk)
        return  rk
        
    def reEncryptPKenc(self, params, rk, cid):
        ciphertext = {'C1':cid['C1'], 'C2':cid['C2']*pair(cid['C1'],rk['R2']), 'C3':rk['R1']}
        if(debug):
            print('ciphertext => ')
            print(ciphertext)
        return ciphertext
    
    def decryptPKenc(self, params, public_key, secret_key, cid):
        Xbytes = pkenc.decrypt(public_key, secret_key, cid['C3'])
        X = bytesToObject(Xbytes, group)          
        m = cid['C2']/pair(cid['C1'],group.hash(X,G1))            
        if(debug):
            print('\nDecrypting...')
            print('m=>')
            print(m)
        return m

    #Jet: Encrypt bytes message 
    def encrypt_jet(self, params, ID, M):
        if type(M) != bytes: raise "Type ERROR: Message should be bytes."
        key = group.random(GT)
        c1 = self.encrypt(params, ID, key)
        # instantiate a symmetric enc scheme from this key
        cipher = AuthenticatedCryptoAbstraction(sha1(key))
        c2 = cipher.encrypt(M)
        return { 'c1':c1, 'c2':c2 }
    #Jet: 
    def decrypt_jet(self, params, skid, cid):
        c1, c2 = cid['c1'], cid['c2']
        key =self.decrypt(params, skid, c1)

        cipher = AuthenticatedCryptoAbstraction(sha1(key))
        return cipher.decrypt(c2)
        
    #Jet:
    def reEncrypt_jet(self, params,rk, cid):
        c1, c2 = cid['c1'], cid['c2']
        ciphertext = self.reEncrypt(params, rk, c1)
        return {'c1':ciphertext, 'c2':c2}
        
    


