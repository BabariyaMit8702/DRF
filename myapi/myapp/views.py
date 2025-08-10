from django.shortcuts import render,HttpResponse
from .serializers import Userserializer,Profileserializer,Postserializer
from rest_framework import viewsets
from django.contrib.auth.models import User
from .models import Profile,Post
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permission import Isonwerorreadonly

# Create your views here.
def home(request):
    return HttpResponse('<h3>GET INFORMATION FROM API</h3>')

class Userinfo(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = Userserializer

class Profileinfo(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = Profileserializer

class Postinfo(viewsets.ModelViewSet,SessionAuthentication):
    queryset = Post.objects.all()
    serializer_class = Postserializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [Isonwerorreadonly]

    def perform_create(self, serializer):
        serializer.save(author_id=self.request.user)



