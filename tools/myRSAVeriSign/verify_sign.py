#!/usr/bin/env python

# from base64 import (
#     b64encode,
#     b64decode,
# )

from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA


def rsa_sign(message, privkey_url): 
    digest = SHA256.new()
    digest.update(message)
    # Read shared key from file
    private_key = False
    with open(privkey_url, "r") as myfile:
        private_key = RSA.importKey(myfile.read())

    # Load private key and sign message
    signer = PKCS1_v1_5.new(private_key)
    sig = signer.sign(digest)
    return sig


def rsa_verify(content, sig, pubkey_url):
    digest = SHA256.new()
    digest.update(content)
    public_key = False
    # Load public key and verify message
    with open(pubkey_url, "r") as pubkey:
        public_key = RSA.importKey(pubkey.read())

    verifier = PKCS1_v1_5.new(public_key)
    verified = verifier.verify(digest, sig)
    try:
        assert verified, 'Signature verification failed'
    except AssertionError:
        return 0
    return 1
    # 'Successfully verified message'


if __name__ == '__main__':
    message = "I want this stream signed"
    priv_url = "private_key.pem"
    pub_url = "public_key.pem"
    rsa_verify(message, rsa_sign(message, priv_url), pub_url)
