# Generated by Django 2.2.6 on 2019-11-15 06:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_auto_20191115_1539'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rating',
            old_name='movie_name',
            new_name='movie',
        ),
    ]