# Generated by Django 3.2.9 on 2021-12-18 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchHistory', '0002_rename_watchhistory_history'),
    ]

    operations = [
        migrations.CreateModel(
            name='movieHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('genre', models.CharField(max_length=120)),
                ('rated', models.IntegerField()),
                ('director', models.CharField(max_length=120)),
                ('type', models.CharField(max_length=120)),
                ('actors', models.CharField(max_length=120)),
                ('languages', models.CharField(max_length=120)),
                ('countries', models.CharField(max_length=120)),
                ('production', models.CharField(max_length=120)),
                ('writers', models.CharField(max_length=120)),
                ('runtime', models.CharField(max_length=120)),
            ],
        ),
        migrations.DeleteModel(
            name='history',
        ),
    ]
