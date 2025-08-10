from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile,Post

class Userserializer(serializers.ModelSerializer):
    #profile_link = serializers.HyperlinkedRelatedField(view_name="profile-detail",read_only=True,source='profile')
    class Meta:
        model = User
        fields = '__all__'

class Postserializer(serializers.HyperlinkedModelSerializer):
    author_name = serializers.CharField(source="author_id.username",read_only=True)
    class Meta:
        model = Post
        fields = '__all__'

class Profileserializer(serializers.HyperlinkedModelSerializer):
    username = serializers.CharField(source="user_id.username",read_only=True)
    posts = serializers.HyperlinkedRelatedField(view_name="post-detail",read_only=True,many=True,source="user_id.posts")
    class Meta:
        model = Profile 
        fields = '__all__'

