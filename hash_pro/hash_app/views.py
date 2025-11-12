from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import json
from . models import Developers
from django.views.decorators.csrf import csrf_exempt
import bcrypt
from .seralizers import Developerseralizer
import jwt
# Create your views here.
def welcome(req):
    return HttpResponse("welcome user")
@csrf_exempt
def register(req):
    if req.method=="POST":
        data=json.loads(req.body)
        u_salt=bcrypt.gensalt(rounds=12)
        password=data["password"].encode("utf-8")
        enc_pass=bcrypt.hashpw(password=password,salt=u_salt)
        dec_pass=enc_pass.decode("utf-8")
        Developers.objects.create(name=data['name'],mail=data['mail'],mobile=data['mobile'],password=dec_pass)
        return JsonResponse({"msg":"registerd successfully"})
def login(req):
    user_data=json.loads(req.body)
    password=user_data["password"]
    id_=user_data["id"]
    print(id_,password)
    data=Developers.objects.get(id=id_)
    seralized_pass=data.password
    is_same=bcrypt.checkpw(password.encode("utf-8"),seralized_pass.encode("utf-8"))
    payloads={
        "name":data.name,
        "email":data.mail

    }
    token=jwt.encode(payload=payloads,key='django-insecure-jjmhy4fguib0-e$+vfm22q=iu061qp)ck7#-*6mgo_(k36jim7',algorithm="HS256")
    print(token)
    T="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoicm9zaGFuIiwiZW1haWwiOiJyb3NoYW5AZ21haWwuY29tIn0.JkFvcpewFaqnl8zDQPoyLfL74xBnm-2sAaGDouQgAdc"
    user=jwt.decode(jwt=T,key='django-insecure-jjmhy4fguib0-e$+vfm22q=iu061qp)ck7#-*6mgo_(k36jim7',algorithms=["HS256"])
    print(user)
    if is_same:
        return HttpResponse("Welcome to the webpage")
    else:
        return HttpResponse("Invalid Credientials")
    

