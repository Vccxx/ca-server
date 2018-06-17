import os
import json
import base64
from tools.myRSAVeriSign.fingerprint import gen
def get_ca_cert():
    file_path = os.path.abspath(__file__)
    file_path =  "/".join(file_path.split("/")[:-1])
    result = {}
    if os.path.exists(file_path+"/cacert"):
        with open(file_path+"/cacert","r") as f:
            for line in f.readlines():
                result[line.split(":")[0]] =line.split(":")[1]
        return json.dumps(result)
    else:
        with open(file_path+"/cacert","w") as f:
            Subject = "Certificatrion Auth Server"
            publickey_path = "/".join(file_path.split("/")[:-1]) + "/myRSAVeriSign"
            PublicKey = ""
            with open(publickey_path + "/public_key.pem","r") as keyfile:
                for lines in keyfile.readlines():
                    if "---" in lines:
                        continue
                    PublicKey += lines.strip()
            PublicKeyAlgorithm = "PKCS1_v1_5"
            Fingerprint = gen(publickey_path+ "/public_key.pem")
            FingerprintAlgorithm = "md5"
            ValidTo = "2019-06-17"
            f.write("Subject:"+Subject + "\n")
            f.write("PublicKey:" + PublicKey + "\n")
            f.write("PublicKeyAlgorithm:" + PublicKeyAlgorithm + "\n")
            f.write("Fingerprint:" + Fingerprint + "\n")
            f.write("FingerprintAlgorithm:" + FingerprintAlgorithm + "\n")
            f.write("ValidTo:"+ValidTo+'\n')
        result["Subject"] = Subject
        result["PublicKey"] = PublicKey
        result["PublicKeyAlgorithm"] = PublicKeyAlgorithm
        result["Fingerprint"] = Fingerprint
        result["FingerprintAlgorithm"] = FingerprintAlgorithm
        result["ValidTo"] = ValidTo
        return json.dumps(result)