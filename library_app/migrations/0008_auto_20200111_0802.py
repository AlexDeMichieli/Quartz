# Generated by Django 3.0.1 on 2020-01-11 08:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library_app', '0007_album_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='albums',
        ),
        migrations.AddField(
            model_name='image',
            name='albums',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, to='library_app.Album'),
            preserve_default=False,
        ),
    ]
