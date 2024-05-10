from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import generics
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from django.contrib.auth.hashers import make_password
from . import permissions as permission
from . import serializers
from chat import models




@api_view(['POST', 'GET'])
@authentication_classes([BasicAuthentication, SessionAuthentication])
@permission_classes([permissions.IsAuthenticated])
def user_create(request):
    username = request.data.get('username')
    password = request.data.get('password')
    phone = request.data.get('phone')
    avatar = ''
    email = ''
    bio = ''
    if request.data.get('avatar'):
        avatar = request.data.get('avatar')
    if request.data.get('email'):
        email = request.data.get('email')
    if request.data.get('bio'):
        bio = request.data.get('bio')
    
    user = models.User.objects.create(
        username=username,
        password=make_password(password),
        phone=phone,
        avatar=avatar,
        email=email,
        bio=bio,
    )
    return Response({
        'created': True
    })


@api_view(['POST'])
@authentication_classes([BasicAuthentication, SessionAuthentication])
@permission_classes([permission.IsOwner])
def user_update(request):
    data = request.data
    serializer = serializers.UserSerializerUpdate(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserList(generics.ListAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializerList
    permission_classes = [permissions.IsAuthenticated]




@api_view(['POST', 'GET'])
@authentication_classes([BasicAuthentication, SessionAuthentication])
@permission_classes([permissions.IsAuthenticated, ])
def group_create(request):
    name = request.data.get('name')
    avatar = request.data.get('avatar')
    description = ''
    if request.data.get('description'):
        description = request.data.get('description')

    group = models.Group.objects.create(
        name=name,
        avatar=avatar,
        description=description,
        author=request.user,
    )

    return Response({
        'created': True
    })


@api_view(['PUT', 'GET'])
@authentication_classes([BasicAuthentication, SessionAuthentication])
@permission_classes([permission.IsGroupOwner])
def group_update(request, code):
    group = models.Group.objects.get(code=code)
    if group.author == request.user:
        group.name = request.data.get('name', group.name)
        group.avatar = request.data.get('avatar', group.avatar)
        group.description = request.data.get('description', group.description)
        group.save()
        return Response({'group_update': 'success'})
    else:
        return Response({'group_update': 'fail'})
    

class GroupList(generics.ListAPIView):
    queryset = models.Group.objects.all()
    serializer_class = serializers.GroupSerializerList
    permission_classes = [permission.IsGroupOwner]



class GroupMemberCreate(generics.CreateAPIView):
    queryset = models.GroupMember.objects.all()
    serializer_class = serializers.GroupMemberSerializerCreate
    permission_classes = [permission.IsGroupOwner]

    def perform_create(self, serializer):
        group_code = self.kwargs.get('group_code')
        group = models.Group.objects.get(code=group_code)
        user = self.request.user
        serializer.save(group=group, user=user)
        

class GroupMemberList(generics.ListAPIView):
    queryset = models.GroupMembers.objects.all()
    serializer_class = serializers.GroupMembersSerializerList
    permission_classes = [permission.IsGroupOwner]


class GroupMemberDetail(generics.RetrieveAPIView):
    queryset = models.GroupMembers.objects.all()
    serializer_class = serializers.GroupMembersSerializerList
    permission_classes = [permission.IsGroupOwner]
