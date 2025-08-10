from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    user_id = models.OneToOneField(User ,on_delete=models.CASCADE)
    bio = models.CharField(max_length=50,default="",blank=True)

    def __str__(self):
        return self.user_id.username
    
class Post(models.Model):
    author_id = models.ForeignKey(User, on_delete=models.CASCADE,related_name="posts")
    title = models.CharField(max_length=50,default="")
    slogun = models.CharField(max_length=30,default="")
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.author_id.username
