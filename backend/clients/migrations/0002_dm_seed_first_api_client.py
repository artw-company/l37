# Generated by Django 4.2 on 2025-03-20 14:10

from clients.models import Client
from common.constants import StatusChoices
from django.db import migrations, transaction


def upgrade(apps, schema_editor):
    with transaction.atomic():
        Client.objects.create_user(
            username="test_api_client", password="lot14password", first_name="Test", status=StatusChoices.ACTIVE.value
        )


def downgrade(apps, schema_editor):
    with transaction.atomic():
        Client.objects.get(username="test_api_client").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("clients", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(upgrade, downgrade),
    ]
