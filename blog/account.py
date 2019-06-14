from django.shortcuts import render,HttpResponse
from blog.models import *
import hashlib
import json

def getmd5pwd(username,password):
    hash = hashlib.sha1()
    pwdstr="blogsite"+password+username+"javafeng"
    bit=pwdstr.encode(encoding='utf-8')
    hash.update(bit)
    return hash.hexdigest()

# Create your views here.
def login(req):
    if req.method != "POST":
        return HttpResponse(json.dumps({"msg":"Method error!","state":0}))
    username = req.POST.get("username").replace(" ","")
    password = req.POST.get("password").strip()
    print(username)
    print(password)
    password=getmd5pwd(username,password)
    print(password)
    users=Account.objects.filter(username=username,password=password)
    if users.count()>0:
        req.session["uid"]=users.first().id
        return HttpResponse(json.dumps({"msg":"Login Success!","state":1}))
    else:
        return HttpResponse(json.dumps({"msg": "Login Error:Wrong username or password!","state":0}))