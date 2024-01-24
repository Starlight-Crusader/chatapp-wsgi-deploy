from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from django.contrib.auth.hashers import make_password

from users.models import User

import random

adjectives = [
    'Happy',       'Clever',
    'Brave',       'Playful',
    'Colorful',    'Mysterious',
    'Vibrant',     'Gentle',
    'Fearless',    'Radiant',
    'Lively',      'Graceful',
    'Dynamic',     'Joyful',
    'Whimsical',   'Serene',
    'Adventurous', 'Charming',
    'Dazzling',    'Spirited',
]

nouns = [
    'Cat',      'Dog',
    'Unicorn',  'Moon',
    'Star',     'Ocean',
    'Mountain', 'Forest',
    'Breeze',   'River',
    'Fire',     'Thunder',
    'Whisper',  'Dream',
    'Rainbow',  'Sunset',
    'Garden',   'Harmony',
    'Phantom',  'Sapphire',
]


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        write_only=True, validators=[]
    )

    class Meta:
        model = User
        fields = ('username', 'password',)
        
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])

        user = User(**validated_data)

        adjective = random.choice(adjectives)
        noun = random.choice(nouns)
        three_digits = random.randint(100, 999)

        user.nickname = f"{adjective}{noun}{three_digits}"
        user.save()

        return user

        
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
