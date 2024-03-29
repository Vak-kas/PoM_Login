# Generated by Django 5.0.1 on 2024-03-06 19:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("signup", "0005_alter_user_user_type"),
    ]

    operations = [
        migrations.CreateModel(
            name="TempEmailVerify",
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
                ("email", models.EmailField(max_length=254, unique=True)),
                ("verification_code", models.CharField(max_length=6)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
