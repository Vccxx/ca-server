# CA服务器 开发文档

## CA服务器：Django实现

### 概述

功能:

- 生成和存储各个网络个体的证书（网络个体包括：电商平台、网上银行和用户)
- 证书的更新和撤销

证书更新(两种更新机制):

- 被动更新	:
  - 浏览器插件检测到某网站证书过期，给CA服务器发送更新请求。
  - CA服务器向该网站服务器发送更新证书请求，告知该网站重新申请证书。
  - 该网站发送新证书申请信息，CA服务器收到并认证之后，颁发新的证书给该网站，同时更新CA服务器本地存储的该网站证书
- 主动更新:
  - CA服务器定期扫描数据库中的证书过期时间，如果过期，就向该网站发送重新申请证书的通知。

证书撤销：

- 若某网站重新申请证书时信息核实不正确或者该网站一直无响应，那么从CA服务器的数据库中撤销该网站的证书。

### 注册(register)

返回消息格式:

```python
#defined in register/tools/DataHandler/DataDefine.py
json.dumps({
  'status_code' :status_code,
  'info':info
})
```

status_code:

```python
#defined in register/tools/DataHandler/DataDefine.py
error_cTom = {
   0: 'SUCCESS',
   1: 'ERR_CHECK_INFO',
   2: 'ERR_PUBLIC_KEY_DUP',
   3: 'ERR_SUBJECT_DUP',# directly update publickey
   4: 'ERR_UNKNOWN',
   5: 'ERR_SN_DUP',
   6: 'ERR_UPDATE',
   7: 'ERR_REVOKE',
   8: 'ERR_REQUIRE'
}#cTom = code To messsage
```

test case:

- testlink(正常请求,成功,返回签名后的证书):

  http://127.0.0.1:8000/ca/register/?Subject=test&PublicKey=testpubk&PublicKeyAlgorithm=a&Fingerprint=testfig&FingerprintAlgorithm=afig

  result:

  ```
  {"info": "{\"PublicKey\": \"testpubk\", \"FingerPrintAlgorithm\": \"afig\", \"PublicKeyAlgorithm\": \"testpubk\", \"FingerPrint\": \"testfig\", \"Signature_Algorithm\": \"PKCS1_v1_5\", \"ValidTo\": \"2018-05-15\", \"SerialNumber\": \"8\", \"Signature\": \"HVZjEwnwVsdYjn2tX7zoBcDFqXnfDoTJtuSV9T7gfpI22Q8GaPut1oURayyVdtNWo8emy4Qa5e2pAwzVDZnJ19zhMNiQ7hzHzTJCMtRrYzqejMoT2J79VkuLegJvw8D0ajZW8oZ3VtOo/awvdDJD9628ZkQVzJBu129wcr6g8hg=\", \"Subject\": \"test\"}", "status_code": 0}
  ```

- testlink(不同用户的公钥重复,返回错误报文):

  http://127.0.0.1:8000/ca/register/?Subject=test1&PublicKey=testpubk&PublicKeyAlgorithm=a&Fingerprint=testfig&FingerprintAlgorithm=afig

  result:

  ```
  {"info": "PublicKey Corruption! Please Gen a new key.", "status_code": 1}
  ```

### 更新(update)

http://127.0.0.1:8000/ca/update/?Subject=test1&PublicKey=testpubk&PublicKeyAlgorithm=a&Fingerprint=testfig&FingerprintAlgorithm=afig

### 撤销(revoke)

http://127.0.0.1:8000/ca/revoke/?Subject=test1

### 查询(require)

http://127.0.0.1:8000/ca/require?Subject=test&Object=test