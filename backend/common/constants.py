from django.db import models


class StatusChoices(models.TextChoices):
    ACTIVE = "active", "активен"
    BLOCKED = "blocked", "заблокирован"


class CommunicationStatusChoices(models.TextChoices):
    SEND = "send", "отправлено"
    FAILED = "failed", "не отправлено"
    RESERVED = "reserved", "забронировано"


class CommunicationDeliveryStatusEnum(models.TextChoices):
    EMPTY = "empty", "Нет статуса"
    DELIVERED = "delivered", "Доставлено"
    VIEWED = "viewed", "Просмотрено"


class CommunicationRuleUnitEnum(models.TextChoices):
    SECOND = "second", "Секунды"
    MINUTE = "minute", "Минуты"
    HOUR = "hour", "Часы"
