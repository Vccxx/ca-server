from ..myRSAVeriSign.verify_sign import rsa_sign,rsa_verify
from enum import Enum
import json
import os
from base64 import b64encode,b64decode
MAX_SERIAL_NUM = 4096

error_cTom = {
   0: 'SUCCESS',
   1: 'ERR_CHECK_INFO',
   2: 'ERR_PUBLIC_KEY_DUP',
   3: 'ERR_SUBJECT_DUP',
   4: 'ERR_UNKNOWN',
   5: 'ERR_SN_DUP',
   6: 'ERR_UPDATE',
   7: 'ERR_REVOKE',
   8: 'ERR_REQUIRE'
}

error_mToc = dict(
    (v,k) for k,v in error_cTom.iteritems()
)

def response_info(status_code,info):
    return json.dumps({
        'status_code' :status_code,
        'info':info
    })

class Certification():
    
    def __init__(self,sNum,sName,pub,pubA,fig,figA,validTo,sign='',signA=''):
        self.snumber = sNum
        self.sname = sName
        self.pk = pub
        self.pka = pubA
        self.fp = fig
        self.fpa = figA
        self.validTo = validTo
        self.sign = sign
        self.signA = signA
    
    def signCert(self):
        #import pdb;pdb.set_trace()
        certContent = self.snumber + self.sname+self.pk+self.pka+self.fp+self.fpa+self.validTo
        path = "/".join(os.path.abspath(__file__).split("/")[:-2])
        
        self.sign = rsa_sign(certContent,path + "/myRSAVeriSign/private_key.pem")
        self.signA = "PKCS1_v1_5"
        return b64encode(self.sign),self.signA
    
    
    def verify(self): 
        certContent = self.snumber + self.sname+self.pk+self.pka+self.fp+self.fpa+self.validTo
        signature=b64decode(self.sign)
        signAri = self.signA
        path = "/".join(os.path.abspath(__file__).split("/")[:-2])
        return rsa_verify(certContent,signature,path+"/myRSAVeriSign/public_key.pem")
        
