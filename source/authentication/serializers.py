from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'last_name', 'first_name', 'password')

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.password = validated_data.get('password', instance.password)

    @staticmethod
    def getJsonVariant(instance):
        return {
            'username': instance.username,
            'email': instance.email,
            'first name': instance.first_name,
            'last name': instance.last_name,
            'complete name': instance.get_full_name(),
            'password': instance.password
        }
