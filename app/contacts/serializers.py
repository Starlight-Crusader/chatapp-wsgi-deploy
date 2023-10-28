from rest_framework import serializers


class AddRemoveContactSerializer(serializers.Serializer):
    contact_nickname = serializers.CharField()
