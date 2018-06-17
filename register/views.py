# -*- coding: utf-8 -*-
from __future__ import unicode_literals 
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from tools.myRSAVeriSign.verify_sign import rsa_sign,rsa_verify
from tools.myRSAVeriSign.reflesh import reflesh_keys  
from tools.myRSAVeriSign.fingerprint import gen
from tools.DataHandler.DataDefine import response_info
from tools.DataHandler.DataDefine import error_mToc
from register.models import Cert
from tools.DataHandler.Validate import *
from tools.DataHandler.Gen import *
from tools.DataHandler.Validate import is_validate
from tools.DataHandler.CACert import get_ca_cert
import datetime
from tools.DataHandler.DataDefine import Certification
from dateutil.relativedelta import relativedelta
import json
# Create your views here.

def register(request):
    sNum = next_sn()
    if not is_validate(request):
        return HttpResponse(response_info(error_mToc["ERR_CHECK_INFO"],"info check wrong"))
    data = {}
    sName = request.GET.get("Subject")
    i = 0
    for i in range(len(Cert.objects.all())):
        if Cert.objects.all()[i].Subject == sName:
            break
    if i >= len(Cert.objects.all()) - 1:
        data['CACERT'] = get_ca_cert()
    
    pub = request.GET.get("PublicKey")
    pubA = request.GET.get("PublicKeyAlgorithm")
    fig = request.GET.get("Fingerprint")
    figA = request.GET.get("FingerprintAlgorithm")
    time = datetime.date.today() + relativedelta(months=+1)
    validTime = time.strftime('%Y-%m-%d')
    ce = Certification(sNum,sName,pub,pubA,fig,figA,validTime)
    sign,signA = ce.signCert()
    c = Cert(SerialNumber=sNum,Subject=sName,PublicKey=pub,PublicKeyAlgorithm=pubA,Fingerprint=fig, 
    		FingerprintAlgorithm=figA,ValidTo=validTime,originSignature=sign,SignatureAlgorithm=signA)
    try:
        c.save()
    except Exception,e:
        print e.message
        if "UNIQUE constraint failed: register_cert.PublicKey" == e.message: 
            return HttpResponse(response_info(error_mToc["ERR_CHECK_INFO"],"PublicKey Corruption! Please Gen a new key."))
        elif "UNIQUE constraint failed: register_cert.SerialNumber" == e.message:
            return HttpResponse(response_info(error_mToc["ERR_SN_DUP"],"Duplicate Serial Number, Contact the admin."))
        else:
            return HttpResponse(response_info(error_mToc["ERR_UNKNOWN"],"UNKNOW Error,Contect the admin."))
    certInfo = {"SerialNumber":sNum,
                "Subject":sName,
                "PublicKey":pub,
                "PublicKeyAlgorithm":pub,
                "FingerPrint":fig,
                "FingerPrintAlgorithm":figA,
                "ValidTo":validTime,
                "Signature":sign,
                "Signature_Algorithm":signA
                }
    certString = json.dumps(certInfo)
    data["certInfo"] = certString
    return HttpResponse(response_info(error_mToc["SUCCESS"],data))

def update(request):
    return HttpResponse(response_info(error_mToc["SUCCESS"],"update success"))

def revoke(request):
    return HttpResponse(response_info(error_mToc["SUCCESS"],"revoke success"))