# Generated by Django 3.0.3 on 2020-04-14 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musica', '0008_podcastepisode_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genre',
            name='id_listenotes',
            field=models.IntegerField(default=0, unique=True),
        ),
    ]