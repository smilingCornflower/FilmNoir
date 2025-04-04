# Generated by Django 5.1.7 on 2025-04-04 09:34

import common.models.base_content
import movie.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("common", "0001_initial"),
        ("movie", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="movie",
            name="genres",
            field=models.ManyToManyField(to="common.genre"),
        ),
        migrations.AlterField(
            model_name="movie",
            name="poster",
            field=models.ImageField(
                upload_to=common.models.base_content._poster_upload_path
            ),
        ),
        migrations.AlterField(
            model_name="movie",
            name="video",
            field=models.FileField(
                blank=True, null=True, upload_to=movie.models._video_upload_path
            ),
        ),
    ]
