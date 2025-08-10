from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


# Create your models here.
class collage(models.Model):
    collage_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30,default="")
    location = models.CharField(max_length=30,default="")
    
    def __str__(self):
        return self.name

class student(models.Model):
    collage_id = models.ForeignKey(collage, on_delete=models.CASCADE , default=6)
    name = models.CharField(max_length=30,default="")
    phone_no = models.CharField(max_length=30,default="")
    address = models.CharField(max_length=30,default="")

    def __str__(self):
        return self.name

class company(models.Model):
    company_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30,default="")
    location = models.CharField(max_length=30,default="")
    type = models.CharField(max_length=30,choices=(('IT','IT'),('NON IT','NON IT'),('MIXED','MIXED')),default='IT')
    about = models.TextField()
    Active = models.BooleanField(default=True)
    added_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class employee(models.Model):
    name = models.CharField(max_length=30,default="")
    email = models.EmailField(default="")
    address = models.TextField()
    phone_no = models.CharField(max_length=22,default="0")
    posotion =  models.CharField(choices=(('manager','MANAGER'),('ml engineer','ML ENGINEER'),('salesman','SALESMAN')),default='salesman',max_length=50)

    company = models.ForeignKey(company,on_delete=models.CASCADE , related_name="employees")

    def __str__(self):
        return self.name
    
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)