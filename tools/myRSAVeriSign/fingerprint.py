import base64
import hashlib

def gen(key_url):
    with open(key_url,"r") as keyfile:
        line = ""
        for lines in keyfile.readlines():
            if "---" in lines:
                continue
            line += lines.strip()
        key = base64.b64decode(line)
        fp_plain = hashlib.md5(key).hexdigest()
        return ':'.join(a+b for a,b in zip(fp_plain[::2], fp_plain[1::2]))
if __name__ == "__main__":
    print gen("public_key.pem")
