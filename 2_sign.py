from tasks import via_openssl_keygen, via_pyopenssl_sign256_key,via_pyopenssl_verify, via_pyopenssl_sign256
import os
import json
import sys
import base64

# 1. Request for generating cert  and write a privte key into a file

# 2  Reqest a signature for the messge by ME
message = b"asdf"

# Get a signature 
message = b"asdf"
id ='alice'
result = via_pyopenssl_sign256.delay(id, message.decode('utf-8'), digest="sha256")
signature = result.get()
print (signature)
