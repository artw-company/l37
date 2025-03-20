from common.constants import CommunicationDeliveryStatusEnum, CommunicationStatusChoices
from communications.models import Communication, CommunicationKind, CommunicationSource
from django.utils.timezone import now
from rest_framework import serializers


class CommunicationKindSerializer(serializers.ModelSerializer):
    """
    Сериализатор для типа комммуникации
    """

    class Meta:
        model = CommunicationKind
        fields = "__all__"


class CommunicationSourceSerializer(serializers.ModelSerializer):
    """
    Сериализатор для канала коммуникации
    """

    class Meta:
        model = CommunicationSource
        fields = "__all__"


class CommunicationSerializer(serializers.ModelSerializer):
    """
    Сериализатор для коммуникации
    """

    class Meta:
        model = Communication
        fields = "__all__"


class CommunicationBookingSerializer(CommunicationSerializer):

    def validate_communication_date(self, value):
        if value < now():
            raise serializers.ValidationError("Время для бронирования должно быть в будущем")
        return value

    def validate_status(self, value):
        if value != CommunicationStatusChoices.RESERVED:
            raise serializers.ValidationError("Неверный статус отложенной коммуникации")
        return value


class CommunicationStatusUpdateSerializer(serializers.ModelSerializer):
    communication_status = serializers.ChoiceField(choices=CommunicationDeliveryStatusEnum.choices, required=True)

    class Meta:
        model = Communication
        fields = ["communication_status"]

    def update(self, instance, validated_data):
        instance.communication_status = validated_data["communication_status"]
        instance.save(update_fields=["communication_status"])
        return instance
