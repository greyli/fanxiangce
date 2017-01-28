from hashlib import sha1
import hmac
import base64
import time
import json
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import urllib2
import os
import pyperclip

def accessKey():
    return 'a4ec1bc90060b71d9b7645509ec4071ffb2ec0d9'

def secretKey():
    return 'da39a3ee5e6b4b0d3255bfef95601890afd80709'

def aid():
    return 1032555

def getToken(param):
    # jsoncode = json.dumps(param)
    # encodedParam = base64.b64encode(jsoncode)
    # sign = hmac.new(secretKey(), encodedParam, sha1).digest()
    # encodedSign = base64.b64encode(sign)
    # Token = accessKey() + ':' + encodedSign + ':' + encodedParam
    return '520a69e999343680d4ae35ead9c877418bd37510:r8xYTTOPfMFUpxLqbALEFxJwHfI=:eyJkZWFkbGluZSI6MTQ4NTQwMjE0OCwiYWN0aW9uIjoiZ2V0IiwidWlkIjoiNTY3NTkxIiwiYWlkIjoiMTI1MzA4NCIsImZyb20iOiJmaWxlIn0='

filename = raw_input()
if os.path.exists(filename) == True:
    register_openers()
    param = {}
    param['deadline'] = int(time.time()) + 60
    param['aid'] = aid()
    Token = getToken(param)
    sendData = {"Token": Token, "file": open(filename, "rb")}
    datagen, headers = multipart_encode(sendData)
    request = urllib2.Request("http://up.tietuku.com/", datagen, headers)
    jsondata = urllib2.urlopen(request).read()
    ret = json.loads(jsondata)
    url = ret[u'linkurl']
    print url
    pyperclip.copy(url)
else:
    print filename + " not exists !"