from django.utils import timezone

from rest_framework import status, response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from app import settings
from .models import Log

import jwt
import os


@api_view(['POST'])
@permission_classes([AllowAny])
def invalid_pin(request):

    try:
        # Get the token
        refresh = request.headers.get('X-Authentication')[len('Bearer '):]

        # Decode the JWT token
        decoded_token = jwt.decode(refresh, settings.SIMPLE_JWT['SIGNING_KEY'], algorithms=['HS256'])

        # Extract the user's id and get the record info to be registered in the consumer instance
        user_id = decoded_token.get('user_id')

        # Register a new log
        new_log = Log(
            code=0,
            timestamp=timezone.now(),
            body=f"U~{user_id}|Invalid PIN entered more than 3 times; the refresh and PIN are dropped; notify user on next successful login",
        )
        new_log.save()

        return response.Response(
            {'message': "Case logged successfully!"},
            status=status.HTTP_200_OK
        )

    except Exception as e:
        return response.Response(
            {'message': "You have to provide some auth. details!"},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_log(request, log_id):
    password = request.headers.get('X-Delete-Password')
    
    if password == os.getenv('DELETE_PASSWORD'):

        try:
            log = Log.objects.get(id=log_id)
            log.delete()

            return response.Response(
                {'message': "Log successfully deleted!"},
                status=status.HTTP_200_OK,
            )
        except:
            return response.Response(
                {'message': "Log not found!"},
                status=status.HTTP_404_NOT_FOUND
            )

    else:

        # Register an unauthorized access attempt
        new_log = Log(
            code=1,
            timestamp=timezone.now(),
            body=f"Unauthorized log deletion request",
            origin_ip=request.META.get('REMOTE_ADDR'),
        )
        new_log.save()

        return response.Response(
            {'message': "You are not authorized to perform this action... an unauthorized access attempt registered!"},
            status=status.HTTP_403_FORBIDDEN,
        )