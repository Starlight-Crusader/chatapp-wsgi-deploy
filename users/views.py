from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import response, status
from django.utils import timezone

from users import serializers
from users.models import User

from logs.models import Log

import os


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def change_nickname(request):    
    user = User.objects.get(id=request.user.id)
    serializer = serializers.UserSerializer(instance=user, data=request.data)

    if serializer.is_valid(raise_exception=True):
        serializer.update_nickname(user, request.data)

    return response.Response(
        {'message': "Nickname successfully updated!"},
        status=status.HTTP_200_OK,
    )


@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_user(request, user_id):
    password = request.headers.get('X-Delete-Password')
    
    if password == os.getenv('DELETE_PASSWORD'):

        try:
            user = User.objects.get(id=user_id)
            user.delete()

            return response.Response(
                {'message': "User successfully deleted!"},
                status=status.HTTP_200_OK,
            )
        except:
            return response.Response(
                {'message': "User not found!"},
                status=status.HTTP_404_NOT_FOUND
            )

    else:

        # Register an unauthorized access attempt
        new_log = Log(
            code=1,
            timestamp=timezone.now(),
            body=f"Unauthorized user deletion request",
            origin_ip=request.META.get('REMOTE_ADDR'),
        )
        new_log.save()

        return response.Response(
            {'message': "You are not authorized to perform this action... an unauthorized access attempt registered!"},
            status=status.HTTP_403_FORBIDDEN,
        )
