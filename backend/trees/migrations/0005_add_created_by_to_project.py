# Generated by Django 4.2.20 on 2025-06-03 04:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("trees", "0004_tree_created_by"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="created_projects",
                to=settings.AUTH_USER_MODEL,
                verbose_name="創建者",
            ),
        ),
    ]
