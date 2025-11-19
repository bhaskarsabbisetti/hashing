from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import json
from . models import Developers
from django.views.decorators.csrf import csrf_exempt
import bcrypt
from .seralizers import Developerseralizer
import jwt
import datetime
from django.conf import settings
from django.core.mail import send_mail,EmailMessage

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
        send_mail(subject="welcome mail",message="Thank you for registerd to our app",recipient_list=[data['mail']],from_email=settings.EMAIL_HOST_USER)
        return JsonResponse({"msg":"registerd successfully"})
@csrf_exempt
def users(req):
    if req.method=="GET":
        try:
            cookie_token=req.COOKIES.get("my_cookie")
            cookie=jwt.decode(jwt=cookie_token,key='django-insecure-jjmhy4fguib0-e$+vfm22q=iu061qp)ck7#-*6mgo_(k36jim7',algorithms=["HS256"])
        except:
            return HttpResponse("no cookie found")
        if cookie["is_valid"]:
            data=Developerseralizer(Developers.objects.all(),many=True)
            return JsonResponse({"users":data.data},safe=False)
        else:
            res=HttpResponse("not a valid user")
            res.delete_cookie("my_cookie")
            return res
    return HttpResponse("only get method works")

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
        "email":data.mail,
        "is_valid":False,
        "id":data.id

    }
    token=jwt.encode(payload=payloads,key='django-insecure-jjmhy4fguib0-e$+vfm22q=iu061qp)ck7#-*6mgo_(k36jim7',algorithm="HS256")
    print(token)
    user=jwt.decode(jwt=token,key='django-insecure-jjmhy4fguib0-e$+vfm22q=iu061qp)ck7#-*6mgo_(k36jim7',algorithms=["HS256"])
    print(user)
    
    if is_same:
        res=HttpResponse("Welcome to the webpage")
        res.set_cookie(
            key="my_cookie",
            value=token,
            httponly=True,
        )
        return res
    else:
        return HttpResponse("Invalid Credientials")
@csrf_exempt
def send_attach(req):
    user_mail=req.POST.get("mail")
    print(user_mail)
    mail=EmailMessage(subject="sending file",body="hello this mail is an test mail",from_email=settings.EMAIL_HOST_USER,to = [user_mail])
    mail.attach_file("C:/Users/bhask/OneDrive/Pictures/Screenshots/Screenshot 2025-11-14 222311.png")
    mail.send()
    return HttpResponse("mail sent successfully")


    

