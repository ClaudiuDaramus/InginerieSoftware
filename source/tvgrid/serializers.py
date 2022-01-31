from rest_framework.serializers import ModelSerializer
from .models import *
from .helpers import validateIntervalOrNone


class ChannelSerializer(ModelSerializer):
    class Meta:
        model = Channel
        fields = ['externalId', 'name', 'country', 'countryCode', 'type']

    def create(self, validated_data=None):
        if validated_data is None:
            validated_data = self.validated_data

        channelType = validated_data.get('type')
        if channelType not in ['web', 'tv']:
            raise Exception('The type of a channel should be web or tv')

        instance = Channel.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data=None):
        if validated_data is None:
            validated_data = self.validated_data
        instance.country = validated_data.get('country')
        instance.save()
        return instance


class ShowSerializer(ModelSerializer):
    class Meta:
        model = Show
        fields = ['externalId', 'name', 'language', 'time', 'rating', 'weight', 'image']

    def create(self, validated_data=None):
        try:
            if validated_data is None:
                validated_data = self.validated_data

            validateIntervalOrNone(validated_data, 'weight', (0, 100))
            validateIntervalOrNone(validated_data, 'rating', (0, 10))

            genres = validated_data.pop('genres')
            days = validated_data.pop('days')

            instance = Show.objects.create(**validated_data)

            if genres is not None:
                instance.genres.clear()

                genres = Genre.objects.filter(name__in=genres).all()
                instance.genres.add(*genres)

            if days is not None:
                instance.days.clear()
                days = Day.objects.filter(name__in=days).all()
                instance.days.add(*days)

            instance.save()
            return instance
        except Exception as e:
            raise e

    def update(self, instance, validated_data=None):
        try:
            if validated_data is None:
                validated_data = self.validated_data

            if validated_data.get('genres'):
                instance.genres.clear()

                genres = Genre.objects.filter(name__in=validated_data['genres']).all()
                instance.genres.add(*genres)

            if validated_data.get('days'):
                instance.days.clear()

                days = Day.objects.filter(name__in=validated_data['days']).all()
                instance.days.add(*days)

            validateIntervalOrNone(validated_data, 'weight', (0, 100))
            validateIntervalOrNone(validated_data, 'rating', (0, 10))

            instance.time = validated_data.get('time', instance.time)
            instance.rating = validated_data.get('rating', instance.rating)
            instance.weight = validated_data.get('weight', instance.weight)
            instance.image = validated_data.get('image', instance.image)

            instance.save()
            return instance
        except Exception as e:
            raise e


class EpisodeSerializer(ModelSerializer):
    class Meta:
        model = Episode
        fields = [
            'externalId', 'name', 'season', 'number', 'startTime', 'endTime', 'rating', 'image',
        ]

    def create(self, validated_data=None):
        try:
            if validated_data is None:
                validated_data = self.validated_data
            validateIntervalOrNone(validated_data, 'rating', (0, 10))

            instance = Episode.objects.create(**validated_data)
            return instance
        except Exception as e:
            raise e

    def update(self, instance, validated_data=None):
        try:
            if validated_data is None:
                validated_data = self.validated_data
            validateIntervalOrNone(validated_data, 'rating', (0, 10))

            instance.startTime = validated_data.get('startTime', instance.startTime)
            instance.endTime = validated_data.get('endTime', instance.endTime)
            instance.image = validated_data.get('image', instance.image)

            instance.save()
            return instance
        except Exception as e:
            raise e


def getOrCreateSimpleBulk(usedModel, nameList):
    if nameList is None:
        return False

    for name in nameList:
        try:
            usedModel.objects.create(name=name)
        except Exception:
            print('Object with name %s already exists' % name)

    return True


def getOrCreateChannel(channelData):
    found = Channel.objects.filter(externalId=channelData['externalId']).first()

    if found is not None:
        return found

    channelSerializer = ChannelSerializer(data=channelData)

    if not channelSerializer.is_valid():
        raise Exception(channelSerializer.error_messages)

    return channelSerializer.create()


def createOrUpdateShow(showData):
    found = Show.objects.filter(externalId=showData['externalId']).first()
    showSerializer = ShowSerializer(data=showData)

    if not showSerializer.is_valid():
        print(showData)
        raise Exception(showSerializer.error_messages)

    showSerializer.validated_data.update({
        'genres': showData['genres'],
        'days': showData['days'],
    })

    if found is None:
        return showSerializer.create()
    else:
        return showSerializer.update(found)


def createOrUpdateBasic(serializerClass, data, modelSettings=(True, True), dynamicFields=[]):
    found = serializerClass.Meta.model.objects.filter(externalId=data['externalId']).first()
    objectSerializer = serializerClass(data=data)
    # print('passed serializer')
    canCreate, canUpdate = modelSettings

    if found is not None and not canUpdate:
        # print('Enter non update-able state')
        return found

    if not objectSerializer.is_valid():
        # print(data)
        raise Exception(objectSerializer.errors)

    updateDict = {}
    for key in dynamicFields:
        updateDict[key] = data[key]

    objectSerializer.validated_data.update(updateDict)

    if found is None and canCreate:
        return objectSerializer.create()
    elif found is not None and canUpdate:
        return objectSerializer.update(found)
