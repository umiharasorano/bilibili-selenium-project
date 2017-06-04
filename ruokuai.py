#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, hashlib, os, random, urllib, urllib.request,operator
from datetime import *

class APIClient(object):
    def http_request(self, url, paramDict):
        post_content = ''
        for key in paramDict:
            post_content = post_content + '%s=%s&'%(key,paramDict[key])
        post_content = post_content[0:-1]
        print (post_content)
        req = urllib.request.Request(url, data=post_content)
        req.add_header('Content-Type', 'application/x-www-form-urlencoded')
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor())
        post_content = post_content.encode()
        response = opener.open(req, post_content)  
        return response.read()
    
    def http_upload_image(self, url, paramKeys, paramDict, filebytes):
        timestr = datetime.now().strftime('%Y-%m-%d %H:%M:%S').encode()
        boundary = '------------' + hashlib.md5(timestr).hexdigest().lower()
        boundarystr = '\r\n--%s\r\n'%(boundary) 
        bs = b''
        for key in paramKeys:
            bs = bs + boundarystr.encode('ascii')
            param = "Content-Disposition: form-data; name=\"%s\"\r\n\r\n%s"%(key, paramDict[key])
            bs = bs + param.encode('utf8')
        bs = bs + boundarystr.encode('ascii')
        header = 'Content-Disposition: form-data; name=\"image\"; filename=\"%s\"\r\nContent-Type: image/gif\r\n\r\n'%('sample')
        bs = bs + header.encode('utf8')
        bs = bs + filebytes
        tailer = '\r\n--%s--\r\n'%(boundary)
        bs = bs + tailer.encode('ascii')
        import requests
        headers = {'Content-Type':'multipart/form-data; boundary=%s'%boundary,
                   'Connection':'Keep-Alive',
                   'Expect':'100-continue',
                   }
        response = requests.post(url, params='', data=bs, headers=headers)
        return response.text[37:-63]

def arguments_to_dict(args):
    argDict = {}
    if args is None:
        return argDict
    
    count = len(args)
    if count <= 1:
        print ('exit:need arguments.')
        return argDict
    
    for i in [1,count-1]:
        pair = args[i].split('=')
        if len(pair) < 2:
            continue
        else:
            argDict[pair[0]] = pair[1]

    return argDict
def isml():
    name = 'isml.png'
    typeid = '3080'
    return name,typeid
def blilbili_ans():
    name = 'blilbili_ans.png'
    typeid = '3040'
    return name,typeid
def blilbili_login():
    name = 'blilbili_login.png'
    typeid = '3050'
    return name,typeid
def blilbili_register():
    name = 'blilbili_register.png'
    typeid = '3050'
    return name,typeid
def mail_163():
    name = 'mail_163.png'
    typeid = '3060'
    return name,typeid
def hotmail_register():
    name = 'hotmail_register.png'
    typeid = '5000'
    return name,typeid
def main(name,typeid):
    client = APIClient()
    paramDict = {}
    result = ''
    act = 'upload'
    if operator.eq(act, 'upload') == 1:
        paramDict['username'] = 'sorano123'
        paramDict['password'] = 'sorano10032'
        paramDict['typeid'] = typeid
        paramDict['timeout'] = '60'
        paramDict['softid'] = '1'
        paramDict['softkey'] = 'b40ffbee5c1cf4e38028c197eb2fc751'
        paramKeys = ['username','password','typeid','timeout','softid','softkey']
        from PIL import Image
        img = Image.open('Captchas\\' + name)
        if img is None:
            print ('get file error!')
        img.save("upload.gif", format="gif")
        filebytes = open("upload.gif", "rb").read()
        result = client.http_upload_image("http://api.ruokuai.com/create.xml", paramKeys, paramDict, filebytes)
    return result
