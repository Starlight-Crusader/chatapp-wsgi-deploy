from rest_framework import serializers

class EncDecSerializer(serializers.Serializer):
    key = serializers.CharField()
    text = serializers.CharField()
