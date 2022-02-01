from rest_framework import serializers
from .models import MediaEntry


class MediaEntrySerializer(serializers.Serializer):
    class Meta:
        model = MediaEntry
        fields = ['channel', 'program', 'description', 'type', 'starting_time', 'duration']

    def create(self, validated_data):
        mediaEntry = MediaEntry.objects.create(**validated_data)
        return mediaEntry

    def update(self, instance, validated_data):
        instance.channel = validated_data.get('channel', instance.channel)
        instance.starting_time = validated_data.get('starting_time', instance.starting_time)
        instance.duration = validated_data.get('duration', instance.duration)
        instance.program = validated_data.get('program', instance.program)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance

    @staticmethod
    def getJsonVariant(instance):
        return {
            'channel': instance.channel,
            'starting time': instance.starting_time,
            'duration': instance.duration,
        }
