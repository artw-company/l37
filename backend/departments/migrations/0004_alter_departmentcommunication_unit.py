# Generated by Django 4.2 on 2025-03-20 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("departments", "0003_alter_departmentcommunication_units_count"),
    ]

    operations = [
        migrations.AlterField(
            model_name="departmentcommunication",
            name="unit",
            field=models.CharField(
                choices=[("second", "Секунды"), ("minute", "Минуты"), ("hour", "Часы")],
                max_length=30,
                verbose_name="Единица времени",
            ),
        ),
    ]
