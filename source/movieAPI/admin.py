from django.contrib import admin
from .models import Genre, Writer, Actor, VideoContent

# Register your models here.
admin.site.register(Genre)
admin.site.register(Writer)
admin.site.register(Actor)
admin.site.register(VideoContent)