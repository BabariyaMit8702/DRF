from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import employee
from django.db.models.signals import post_save,post_delete,pre_delete,pre_save

# @receiver(user_logged_in,sender=User)
# def on_lin(sender,request,**kwargs):
#     print('loged in succussfully')
    
@receiver(post_save,sender=employee)
def ae(sender,instance,created,**kwargs):
    if(created):
        print('add new one')
    else:
        print('updated one')