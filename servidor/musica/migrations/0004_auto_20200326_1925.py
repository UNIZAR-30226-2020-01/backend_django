# Generated by Django 3.0.3 on 2020-03-26 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musica', '0003_auto_20200322_2051'),
    ]

    operations = [
        migrations.AddField(
            model_name='folder',
            name='icon',
            field=models.FileField(blank=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='list',
            name='icon',
            field=models.FileField(blank=True, upload_to=''),
        ),
    ]
