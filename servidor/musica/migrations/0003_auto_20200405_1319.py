# Generated by Django 3.0.3 on 2020-04-05 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musica', '0002_auto_20200405_1238'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='number_albums',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='artist',
            name='number_songs',
            field=models.IntegerField(default=0),
        ),
    ]
