# Generated by Django 5.0.1 on 2024-02-10 03:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("signup", "0003_rename_idx_user_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="enterprise",
            name="company_code",
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]
