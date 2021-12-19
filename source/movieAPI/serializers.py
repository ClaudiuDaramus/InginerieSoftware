from rest_framework import serializers
from .models import VideoContent, Genre, Writer, Actor


class VideoContentSerializer(serializers.Serializer):
    class Meta:
        model = VideoContent
        fields = ('imdbID','title', 'year', 'rated', 'released', 'runtime', 'plot')
# ////////////
# title = models.CharField(max_length=100)
# year = models.CharField(max_length=20)
# rated = models.CharField(max_length=10)
# released = models.DateField()  # '%Y-%m-%d
# runtime = models.IntegerField(null=True)
# genres = models.ManyToManyField(Genre)
# director = models.CharField(max_length=20, null=True)
# writers = models.ManyToManyField(Writer)
# actors = models.ManyToManyField(Actor)
# plot = models.CharField(max_length=1500)
# ///////////////

    def create(self, validated_data):
        print(validated_data)
        genres = validated_data.pop("genres")
        writers = validated_data.pop("writers")
        actors = validated_data.pop("actors")

        video = VideoContent.objects.create(**validated_data)
        for writer in writers:
            found = Writer.objects.filter(name = writer).first()
            if found is None:
                found = Writer.objects.create(writer = writer)
            video.genres.add(found)
        for genre in genres:
            found = Genre.objects.filter(name=genre).first()
            if found is None:
                found = Genre.objects.create(genre=genre)
            video.genres.add(found)
        for actor in actors:
            found = Actor.objects.filter(name=actor).first()
            if found is None:
                found = Actor.objects.create(actor=actor)
            video.genres.add(found)
        return video

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.year = validated_data.get('year', instance.year)
        instance.rated = validated_data.get('rated', instance.rated)
        instance.runtime = validated_data.get('runtime', instance.runtime)
        instance.plot = validated_data.get('plot', instance.plot)
        instance.save()
        return instance

    @staticmethod
    def getJsonVariant(instance):
        return {
            'title': instance.title,
            'year': instance.year,
            'rated': instance.rated,
            'runtime': instance.runtime,
            'plot': instance.plot
        }

