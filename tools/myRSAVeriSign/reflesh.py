import os
def reflesh_keys():
    # Generate RSA private key
    os.system("openssl genrsa -out private_key.pem 1024")
    os.system("openssl rsa -in private_key.pem -outform PEM -pubout -out public_key.pem")
