# Generated by Django 3.0.6 on 2020-05-20 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musica', '0015_s7_user_favorito'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='times_faved',
            field=models.IntegerField(default=0),
        ),
    ]
