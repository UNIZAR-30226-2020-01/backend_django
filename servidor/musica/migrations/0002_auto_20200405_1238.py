# Generated by Django 3.0.3 on 2020-04-05 12:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('musica', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='playlist',
            name='folders',
        ),
        migrations.AddField(
            model_name='folder',
            name='playlists',
            field=models.ManyToManyField(to='musica.Playlist'),
        ),
        migrations.AlterField(
            model_name='album',
            name='artist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='albums', to='musica.Artist'),
        ),
        migrations.AlterField(
            model_name='folder',
            name='user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='musica.S7_user'),
        ),
    ]