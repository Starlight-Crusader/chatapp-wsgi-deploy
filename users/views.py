from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import response, status

from users import serializers
from users.models import User


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def change_nickname(request):    
    user = User.objects.get(id=request.user.id)
    serializer = serializers.UpdateNicknameSerializer(instance=user, data=request.data)

    if serializer.is_valid(raise_exception=True):
        serializer.update_nickname(user, request.data)

    return response.Response(
        {'message': 'Nickname successfully updated!'},
        status=status.HTTP_200_OK
    )

 
@api_view(['PATCH'])
@permission_classes([AllowAny])
def change_password(request):
    serializer = serializers.UpdatePasswordSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        serializer.update_password(request.data)

    return response.Response(
        {'message': 'Password successfully updated!'},
        status=status.HTTP_200_OK
    )
 
 
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    serializer = serializers.DeleteUserSerializer(data=request.data, context={'user': request.user})

    if serializer.is_valid(raise_exception=True):
        serializer.delete(request.user)

    return response.Response(
        {'message': 'User successfully deleted!'},
        status=status.HTTP_200_OK
    )


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def go_online(request):
    user = User.objects.get(id=request.user.id)
    user.online = True
    user.save()

    return response.Response(
        {'message': "Successfully set user's status to online!"},
        status=status.HTTP_200_OK
    )


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def go_offline(request):
    user = User.objects.get(id=request.user.id)
    user.online = False
    user.save()

    return response.Response(
        {'message': "Successfully set modified user's status to offline!"},
        status=status.HTTP_200_OK
    )
