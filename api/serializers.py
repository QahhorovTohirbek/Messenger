from rest_framework import serializers, viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.permissions import BasePermission
from django.contrib.auth.models import User
from chat.models import *




class UserSerializerCreate(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username',  'password', 'phone', 'avatar', 'bio']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class UserSerializerList(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class UserImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserImages
        fields = ['id', 'user', 'image']


class GroupSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = [ 'name', 'description', 'image', 'author']


class GroupSerializerList(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']


class GroupMembersSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = GroupMembers
        fields = ['group', 'user']


class GroupMembersSerializerList(serializers.ModelSerializer):
    class Meta:
        model = GroupMembers
        fields = ['group', 'user']


class SentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SentRequest
        fields = ['user', 'group', 'status']


class MessegeSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = [ 'user', 'group_message', 'content']

        
class MessegeSerializerList(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['content']


class MessageFiles(serializers.ModelSerializer):
    class Meta:
        model = MessageFiles
        fields = ['messege', 'file']











