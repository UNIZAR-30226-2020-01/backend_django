# Generated by Django 3.0.6 on 2020-05-27 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musica', '0018_genre_number_podcasts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genre',
            name='number_podcasts',
            field=models.IntegerField(default=0),
        ),
    ]