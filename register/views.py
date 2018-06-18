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
from tools.DataHandler.Validate import is_validate,is_validate_subject
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
                "Fingerprint":fig,
                "FingerprintAlgorithm":figA,
                "ValidTo":validTime,
                "Signature":sign,
                "Signature_Algorithm":signA
                }
    certString = json.dumps(certInfo)
    data["certInfo"] = certString
    return HttpResponse(response_info(error_mToc["SUCCESS"],data))

def update(request):
    sName = request.GET.get("Subject")
    for i in range(len(Cert.objects.all())):
        if Cert.objects.all()[i].Subject == sName:
            return register(request) 
    return HttpResponse(response_info(error_mToc["ERR_UPDATE"],"You need to regist first."))

def revoke(request):
    sName = request.GET.get("Subject")
    if not is_validate_subject(sName):
        return HttpResponse(response_info(error_mToc["ERR_REVOKE"],"Invalid Subject,You are not allowed to revoke."))
    for i in range(len(Cert.objects.all())):
        if Cert.objects.all()[i].Subject == sName:
            try:
                Cert.objects.get(Subject = sName).delete()
            except Exception,e:
                return HttpResponse(response_info(error_mToc["ERR_REVOKE"],e.message))
            return HttpResponse(response_info(error_mToc["SUCCESS"],"Revoke Success!"))
    return HttpResponse(response_info(error_mToc["ERR_REVOKE"],"You don't have a Cert Recode Now. Regist first."))

def require(request):
    sName = request.GET.get("Subject")
    oName = request.GET.get("Object")
    if sName == '' or oName == '' or sName == None or oName==None:
        return HttpResponse(response_info(error_mToc["ERR_REQUIRE"],"Subject and Object segment Required!"))
    for i in range(len(Cert.objects.all())):
        if Cert.objects.all()[i].Subject == sName:
            cert_info = {}
            for j in range(len(Cert.objects.all())):
                if Cert.objects.all()[j].Subject == oName:
                    cert_info["SerialNumber"] = Cert.objects.all()[j].SerialNumber
                    cert_info["Subject"] = Cert.objects.all()[j].Subject
                    cert_info["PublicKey"] = Cert.objects.all()[j].PublicKey
                    cert_info["PublicKeyAlgorithm"] = Cert.objects.all()[j].PublicKeyAlgorithm
                    cert_info["Fingerprint"] = Cert.objects.all()[j].Fingerprint
                    cert_info["FingerprintAlgorithm"] = Cert.objects.all()[j].FingerprintAlgorithm
                    cert_info["ValidTo"] = Cert.objects.all()[j].ValidTo.strftime('%Y-%m-%d')
                    cert_info["Signature"] = Cert.objects.all()[j].originSignature
                    cert_info["SignatureAlgorithm"] = Cert.objects.all()[j].SignatureAlgorithm
                    break
            if cert_info == {}:
                return  HttpResponse(response_info(error_mToc["ERR_REQUIRE"],"Invalid Object"))
            return HttpResponse(response_info(error_mToc["SUCCESS"],json.dumps(cert_info)))
    return HttpResponse(response_info(error_mToc["ERR_REQUIRE"],"Invalid Subject"))

                    
    