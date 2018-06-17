# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from tools.DataHandler.DataDefine import MAX_SERIAL_NUM
from django.db import models

# Create your models here.

class Cert(models.Model):
    SerialNumber = models.CharField(max_length = MAX_SERIAL_NUM,unique=True)#公钥标识号,1~9223372036854775807
    Subject = models.CharField(max_length = 128,primary_key = True)# 公钥拥有者
    PublicKey = models.CharField(max_length = 4096,unique=True) #公钥
    PublicKeyAlgorithm = models.CharField(max_length = 128) #公钥生成算法.
    Fingerprint = models.CharField(max_length = 2048)# 公钥指纹.
    FingerprintAlgorithm = models.CharField(max_length = 128)# 公钥指纹生成算法。
    ValidTo = models.DateField()# 公钥失效日期.
    originSignature = models.CharField(max_length=4096)#CA服务器的初始私钥签名
    SignatureAlgorithm = models.CharField(max_length=128)# 签名算法.