# Generated by Django 4.1 on 2024-04-04 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("communications", "0002_alter_communication_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="communication",
            name="message",
            field=models.TextField(default="", verbose_name="Текст сообщения"),
        ),
        migrations.AlterField(
            model_name="communication",
            name="communication_date",
            field=models.DateTimeField(verbose_name="Дата коммуникации"),
        ),
    ]
