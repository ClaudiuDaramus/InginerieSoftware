from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'last_name', 'first_name', 'password')
        fieldsNormalized = ('username', 'email', 'last name', 'first name', 'password')

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
        instance.save()
        return instance

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


# when we add history for the profile we need to update the serializer
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('profileName',)
        fieldsNormalized = ('profile name',)

    def create(self, validated_data):
        profile = Profile.objects.create(**validated_data)
        return profile

    def update(self, instance, validated_data):
        instance.profileName = validated_data.get('profileName', instance.profileName)
        instance.save()
        return instance

    @staticmethod
    def getJsonVariant(instance):
        return {
            'profile name': instance.profileName,
            'user id': instance.user.pk,
            'creation date': instance.creationDate,
        }
