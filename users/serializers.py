from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from django.contrib.auth.hashers import check_password, make_password

from users.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('nickname', 'online',)


class UpdateNicknameSerializer(serializers.Serializer):
    nickname = serializers.CharField(
        required=True,    
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ('nickname')

    def update_nickname(self, instance, validated_data):
        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.save()

        return instance


class UpdatePasswordSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
    )

    new_password = serializers.CharField(
        write_only=True, required=True, validators=[]
    )

    secret = serializers.CharField(
        write_only=True, required=True, validators=[]
    )

    class Meta:
        model = User,
        fields = ('username', 'new_password', 'secret')
        
    def validate(self, attrs):
        try:
            user = User.objects.get(username=attrs.get('username'))
        except User.DoesNotExist:
            raise serializers.ValidationError('User not found.')
        
        if not check_password(attrs.get('secret'), user.secret):
            raise serializers.ValidationError('Invalid secret.')

        return super().validate(attrs)
    
    def update_password(self, validated_data):
        try:
            user = User.objects.get(username=validated_data.get('username'))
        except User.DoesNotExist:
            raise serializers.ValidationError('User not found.')

        user.password = make_password(validated_data.get('new_password'))
        user.save()

        return user


class DeleteUserSerializer(serializers.Serializer):
    secret = serializers.CharField(
        write_only=True, required=True, validators=[]
    )

    def validate(self, data):
        user = self.context.get('user')
        if not check_password(data.get('secret'), user.secret):
            raise serializers.ValidationError('Invalid secret.')

        return super().validate(data)

    def delete(self, instance):
        instance.delete()
