from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from django.contrib.auth.hashers import make_password

from users.models import User


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        write_only=True, validators=[]
    )

    secret = serializers.CharField(
        write_only=True, validators=[]
    )

    nickname = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ('username', 'password', 'secret', 'nickname')
        
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        validated_data['secret'] = make_password(validated_data['secret'])

        user = User(**validated_data)
        user.save()

        return user

        
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
