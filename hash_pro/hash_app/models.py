from django.db import models

# Create your models here.
class Developers (models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=20)
    mail=models.EmailField(unique=True)
    mobile=models.IntegerField(unique=True,max_length=10)
    password=models.CharField(default="1234",max_length=100)
