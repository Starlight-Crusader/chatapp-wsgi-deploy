from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import response, status

from .serializers import RegisterSerializer, LoginSerializer
from users.models import User

from rest_framework_simplejwt.tokens import RefreshToken


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    try:
        if len(serializer.validated_data['password']) < 8:
            return response.Response(
                {'message': "This password is too short!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save()
        return response.Response(
            {'message': "User registered successfully!"},
            status=status.HTTP_201_CREATED,
        )
    except:
        return response.Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    try:
        user = User.objects.get(username=serializer.data['username'])

        if not user.check_password(serializer.data['password']):
            return response.Response(
                {'message': "Provided auth credentials are incorrect!"},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    except User.DoesNotExist:
        return response.Response(
            {'message': "User not found!"},
            status=status.HTTP_404_NOT_FOUND
        )
    
    refresh = RefreshToken.for_user(user=user)
    tokens = {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

    return response.Response(
        {
            'tokens': tokens,
            'nickname': user.nickname,
        },
        status=status.HTTP_202_ACCEPTED,
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_token(request):
    return response.Response(
        {'msg': "Token is still valid, welcome back " + request.user.nickname + '!'},
        status=status.HTTP_200_OK
    )
