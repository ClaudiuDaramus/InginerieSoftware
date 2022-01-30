from musicAPI.models import Song, ExternalLink, RedirectLink
# class SongSerializer(serializers.ModelSerializer):
#     external_links = serializers.PrimaryKeyRelatedField(many=True, queryset=ExternalLink.objects.all())
#     redirect_links = serializers.PrimaryKeyRelatedField(many=True, queryset=RedirectLink.objects.all())
#     class Meta:
#         model = Song
#         fields = ['shazam_key', 'title', 'artist', 'cover', 'external_links', 'redirect_links']
