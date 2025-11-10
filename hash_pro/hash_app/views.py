from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import json
from . models import Developers
from django.views.decorators.csrf import csrf_exempt
import bcrypt
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