from tasks import via_openssl_keygen, via_pyopenssl_sign256_key,via_pyopenssl_verify, via_pyopenssl_sign256
import os
import json
import sys
import base64

# 1. Request for generating cert  and write a privte key into a file
id = 'alice'
passphrase = 'hello'
result = via_openssl_keygen.delay(id, passphrase)
priv_key = result.get()
bkey = base64.b64decode(priv_key)
skey = bkey.decode('utf-8')
print(skey)

prv_key_file='temp.pem'
with open(prv_key_file, 'wb') as key_file:
     binary_format = bytearray(bkey)
     key_file.write(binary_format)
     key_file.close()

'''
# 2 : working
message = b"asdf"
result = via_pyopenssl_sign256_key.delay(message.decode('utf-8'), priv_key,  digest="sha256")
signature = result.get()
'''

# 2
#prv_key_file='key1.pem'
message = b"asdf"

# Get a signature 
message = b"asdf"
result = via_pyopenssl_sign256.delay(message.decode('utf-8'), digest="sha256")
signature = result.get()

'''
signature_file='signature.sig'
print ("send a message with signiture")
with open(signature_file, 'rb') as f:
      signature = f.read()
print (type(signature))
'''

# Verify a message with a signature
#message = b"XXXX"
message = b"asdf"
#message = base64.b64encode(message)
result = via_pyopenssl_verify.delay(signature, message.decode('utf-8'), digest="sha256")
status = result.get()
print ("verifying status = {}".format(status))


