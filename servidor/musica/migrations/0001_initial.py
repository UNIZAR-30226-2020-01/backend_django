# Generated by Django 3.0.3 on 2020-04-07 16:02

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(blank=True, max_length=50)),
                ('image', models.FileField(blank=True, null=True, upload_to='')),
                ('biography', models.TextField(blank=True)),
            ],
            options={
                'db_table': 'Artist',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Audio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('file', models.FileField(blank=True, null=True, upload_to='')),
            ],
            options={
                'db_table': 'Audio',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'Genre',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Podcast',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('RSS', models.FileField(upload_to='')),
                ('genre', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='musica.Genre')),
            ],
            options={
                'db_table': 'Podcast',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='S7_user',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('segundos', models.IntegerField(default=0, null=True)),
                ('favorito', models.ManyToManyField(blank=True, related_name='favorito', to='musica.Audio')),
                ('podcasts', models.ManyToManyField(blank=True, to='musica.Podcast')),
                ('reproduciendo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='musica.Audio')),
                ('siguiendo', models.ManyToManyField(blank=True, related_name='seguidor', to='musica.S7_user')),
            ],
            options={
                'db_table': 'S7_user',
                'managed': True,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, unique=True)),
                ('icon', models.FileField(blank=True, upload_to='')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='musica.S7_user')),
            ],
            options={
                'db_table': 'Playlist',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, unique=True)),
                ('icon', models.FileField(blank=True, upload_to='')),
                ('playlists', models.ManyToManyField(related_name='folder', to='musica.Playlist')),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='musica.S7_user')),
            ],
            options={
                'db_table': 'Folder',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('date', models.DateField(db_column='fecha')),
                ('icon', models.FileField(blank=True, upload_to='')),
                ('type', models.CharField(choices=[('N', 'Normal'), ('EP', 'EP'), ('S', 'Single')], max_length=2)),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='albums', to='musica.Artist')),
                ('other_artists', models.ManyToManyField(blank=True, related_name='featured_in_album', to='musica.Artist')),
            ],
            options={
                'db_table': 'Album',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('audio_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='musica.Audio')),
                ('track', models.IntegerField()),
                ('times_played', models.IntegerField(default=0)),
                ('lyrics', models.TextField(blank=True)),
                ('duration', models.IntegerField(default=0)),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='songs', to='musica.Album')),
            ],
            options={
                'db_table': 'Song',
                'managed': True,
            },
            bases=('musica.audio',),
        ),
        migrations.CreateModel(
            name='PodcastEpisode',
            fields=[
                ('audio_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='musica.Audio')),
                ('URI', models.FileField(upload_to='')),
                ('podcast', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='musica.Podcast')),
            ],
            options={
                'db_table': 'PodcastEpisode',
                'managed': True,
            },
            bases=('musica.audio',),
        ),
        migrations.AddField(
            model_name='playlist',
            name='songs',
            field=models.ManyToManyField(blank=True, to='musica.Song'),
        ),
    ]
