# Generated by Django 3.0.3 on 2020-04-01 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musica', '0002_auto_20200401_1742'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='lyrics',
            field=models.TextField(blank=True),
        ),
    ]
