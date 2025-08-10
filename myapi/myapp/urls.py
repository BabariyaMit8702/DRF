from django.contrib import admin
from django.urls import path,include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'users',views.Userinfo,basename='user')
router.register(r'profiles',views.Profileinfo,basename='profile')
router.register(r'posts',views.Postinfo,basename='post')

urlpatterns = [
    path('',include(router.urls)),
    path('auth/',include('rest_framework.urls')),
]