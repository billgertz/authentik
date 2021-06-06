# Generated by Django 3.2.3 on 2021-05-29 22:14

import uuid

import django.db.models.deletion
from django.apps.registry import Apps
from django.conf import settings
from django.db import migrations, models
from django.db.backends.base.schema import BaseDatabaseSchemaEditor

import authentik.core.models


def migrate_sessions(apps: Apps, schema_editor: BaseDatabaseSchemaEditor):
    db_alias = schema_editor.connection.alias
    from django.contrib.sessions.backends.cache import KEY_PREFIX
    from django.core.cache import cache

    session_keys = cache.keys(KEY_PREFIX + "*")
    cache.delete_many(session_keys)


class Migration(migrations.Migration):

    dependencies = [
        ("authentik_core", "0021_alter_application_slug"),
    ]

    operations = [
        migrations.CreateModel(
            name="AuthenticatedSession",
            fields=[
                (
                    "expires",
                    models.DateTimeField(
                        default=authentik.core.models.default_token_duration
                    ),
                ),
                ("expiring", models.BooleanField(default=True)),
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                ("session_key", models.CharField(max_length=40)),
                ("last_ip", models.TextField()),
                ("last_user_agent", models.TextField(blank=True)),
                ("last_used", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.RunPython(migrate_sessions),
    ]