from celery import Celery
from bson.objectid import ObjectId
from bson import json_util
import sys

import subprocess
import tempfile

import cryptography.exceptions
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
import base64
from cryptography.hazmat.primitives import hashes

app = Celery('tasks', backend='rpc://',  broker='pyamqp://')

PEM = (b"""-----BEGIN RSA PRIVATE KEY-----
-----END RSA PRIVATE KEY-----""")
@app.task
def via_openssl_keygen(id,message):
    message = message.encode()
    with open(id+".pem", "wb+") as f:
        f.write(PEM)
        f.flush()
        p = subprocess.Popen("openssl genrsa -out " + f.name, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    stdout, stderr = p.communicate(input=message)
    if stderr or p.returncode != 0:
        print(stderr)

    with open(id+ ".pub", "wb+") as f1:
        f1.write(PEM)
        f1.flush()
        p = subprocess.Popen("openssl rsa -in " + f.name + " -pubout > " + f1.name, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    stdout, stderr = p.communicate(input=message)
    if stderr or p.returncode != 0:
        print(stderr)
#    return "error"


    import OpenSSL.crypto
    c=OpenSSL.crypto
    #with open(prv_key_file, 'rb') as key_file:
    prv_key_file = id +'.pem' 
    with open(prv_key_file, 'rb') as key_file:
           st_key=key_file.read()
           key=c.load_privatekey(c.FILETYPE_PEM, st_key)
    key = base64.b64encode(st_key)
    return key.decode('utf-8')



prv_key_file='alice.pem'
@app.task
def via_pyopenssl_sign256(id, message, digest="sha256"):
    message = message.encode()
    prv_key_file = id +".pem"
    with open(prv_key_file, 'rb') as key_file:
        key = load_pem_private_key(
           key_file.read(),
           password = None,
           backend = default_backend(),
        )
    # Sign the payload file.
    sign = base64.b64encode(
       key.sign(
          message,
          padding.PSS(
             mgf = padding.MGF1(hashes.SHA256()),
             salt_length = padding.PSS.MAX_LENGTH,
          ),
          hashes.SHA256(),
      )
    )
    return sign.decode('utf-8')
'''
    with open(signature_file, 'wb') as f:
        f.write(sign)
    return sign
'''

@app.task
def via_pyopenssl_sign256_key(message, pkey, digest="sha256"):
    message = message.encode()
    key = load_pem_private_key(
           pkey,
           password = None,
           backend = default_backend(),
    )
    # Sign the payload file.
    sign = base64.b64encode(
       key.sign(
          message,
          padding.PSS(
             mgf = padding.MGF1(hashes.SHA256()),
             salt_length = padding.PSS.MAX_LENGTH,
          ),
          hashes.SHA256(),
      )
    )
    return sign.decode('utf-8')

pub_key_file='key1.pub'
@app.task
def via_pyopenssl_verify(id, signature, message, digest="sha256"):
    signature = base64.b64decode(signature)
    message = message.encode()
    pub_key_file = id +'.pub'
    public_key = load_pem_public_key(open(pub_key_file, 'rb').read(),default_backend())
    # Perform the verification.
    
    try:
       ret = public_key.verify(
          signature,
          #b"plaintextMessage",
          message,
          padding.PSS(
             mgf = padding.MGF1(hashes.SHA256()),
             salt_length = padding.PSS.MAX_LENGTH,
          ),
          hashes.SHA256())
       #print (ret)
       return "verified"
    except cryptography.exceptions.InvalidSignature as e:
       print('ERROR: Payload and/or signature files failed verification!')
       return "not verified"

