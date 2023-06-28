# Generated by Django 4.2.2 on 2023-06-28 05:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import user.models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("username", models.CharField(max_length=25, unique=True)),
                ("bio", models.TextField(max_length=200)),
                (
                    "image",
                    models.ImageField(
                        blank=True, null=True, upload_to=user.models.profile_picture
                    ),
                ),
                (
                    "followers",
                    models.ManyToManyField(
                        blank=True,
                        null=True,
                        related_name="followers",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "following",
                    models.ManyToManyField(
                        blank=True,
                        null=True,
                        related_name="following",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
