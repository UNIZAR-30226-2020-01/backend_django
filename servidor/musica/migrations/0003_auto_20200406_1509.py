# Generated by Django 3.0.3 on 2020-04-06 15:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('musica', '0002_playlist_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='folder',
            name='playlists',
            field=models.ManyToManyField(related_name='folder', to='musica.Playlist'),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='user',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='musica.S7_user'),
            preserve_default=False,
        ),
    ]
