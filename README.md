# CA服务器+客户端 开发文档

## SGuarder：firefox浏览器插件

#### 1. 首次安装运行时，要求用户输入信息 

为了生成用户的合法证书，SGuarder被首次安装时，会要求用户输入：

- 基本身份信息——用于申请用户证书和生成公私钥对
- 认证密码——用于加密私钥存储在本地，每次交易时需要输入认证密码来确保此次交易由本人发起

SGuarder本地存储着CA服务器的初始公钥。

> 初始公钥:仅用于SGuarder和CA服务器首次交互更新公钥时CA服务器身份的验证。

首次连网时，SGuarder向CA请求当前公钥，存储在本地，公钥格式：

~~~
Serial Number:公钥标识号
Subject: 公钥拥有者
Public Key: 公钥
Public Key Algorithm: 公钥生成算法.
Fingerprint: 公钥指纹.
Fingerprint Algorithm: 公钥指纹生成算法。
Valid-To: 公钥失效日期.
origin-Signature :CA服务器的初始私钥签名
Signature Algorithm: 签名算法.
~~~

#### 2.每次访问银行或交易平台的网站时，验证该网站证书的合法性 

交易平台或银行将从CA服务器获取的证书通过HTTP请求中的字段传到用户的浏览器，SGuarder从请求头中获取证书，进行验证：

- 若证书合法，则显示绿色提示：当前网站安全，可以放心使用
- 若证书不合法，则显示红色提示：当前网站不安全，请联系网站开发者及时更新证书；若是由证书过期引起的证书不合法，则提示CA服务器更新当前网站证书。

网站（或用户）证书格式模仿X.509，具体字段及其说明如下：

~~~
Serial Number: 证书的标识号
Subject: 标识证书的拥有者，比如持有此证书的组织名称.
Issuer: 证书的签发实体。
Subject Alt Name Extension: 这个证书可以认证的网站地址的列表（对于个体用户来说，这个字段存储用户基本信息，包括身份证号和姓名）
Signature: 证书签发实体的签名。
Signature Algorithm: 签名算法.
Valid-From: 证书签发日期。
Valid-To: 证书失效日期.
Key-Usage and Extended Key Usage: 定义了证书可以如何被使用，例如确定一个网站的所有者（web服务器身份认证）。
Public Key: 网站（个人）公钥
Public Key Algorithm: 公钥生成算法.
Fingerprint: 公钥指纹.
Fingerprint Algorithm: 公钥指纹生成算法。 
~~~

#### 3. 参与双签名的生成

用户在交易平台上点击“确认付款”时，需要用户私钥参与签名，而用户私钥是使用用户的认证密码加密存储在本地的。因此用户每次交易前需要输入认证密码，密码正确才提取用户的私钥，进行签名，这样保证了用户对于订单信息的不可抵赖性。

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

-  若某网站重新申请证书时信息核实不正确或者该网站一直无响应，那么从CA服务器的数据库中撤销该网站的证书。

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
   4: 'ERR_UNKNOWN'
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



### 被动更新(update)



###撤销(revoke) 

