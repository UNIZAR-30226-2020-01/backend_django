# Generated by Django 3.0.3 on 2020-04-13 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musica', '0007_auto_20200413_2113'),
    ]

    operations = [
        migrations.AddField(
            model_name='podcastepisode',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
