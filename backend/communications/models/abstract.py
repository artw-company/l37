from common.constants import StatusChoices
from django.db import models


class CommunicationAbstract(models.Model):
    """
    Абстрактный класс для коммуникаций
    """

    name = models.CharField(max_length=100, verbose_name="Название")
    status = models.CharField(max_length=30, choices=StatusChoices.choices, verbose_name="Статус")

    class Meta:
        abstract = True

    def __str__(self):
        return self.name
