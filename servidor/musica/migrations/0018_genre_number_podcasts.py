# Generated by Django 3.0.6 on 2020-05-27 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musica', '0017_s7_user_icon'),
    ]

    operations = [
        migrations.AddField(
            model_name='genre',
            name='number_podcasts',
            field=models.IntegerField(default=0, unique=False),
        ),
    ]
