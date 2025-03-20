from common.constants import StatusChoices
from rest_framework import serializers
from users.models import CustomUser, CustomUserCommunication


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели пользователя
    """

    class Meta:
        model = CustomUser
        fields = "__all__"


class CustomCreateUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор создания модели пользователя
    """

    activity = serializers.CharField(
        source="user_communications.status", label="Активность пользователя", default="active"
    )

    def create(self, validated_data):

        activity_block: dict = validated_data.pop("user_communications", {})
        activity: str = activity_block.get("status")
        instance: CustomUser = super().create(validated_data=validated_data)
        CustomUserCommunication.objects.update_or_create(user=instance, defaults={"status": activity})
        return instance

    def to_representation(self, instance):
        ret: dict = super().to_representation(instance=instance)
        try:
            user_communication: CustomUserCommunication = CustomUserCommunication.objects.get(user=instance)
        except CustomUserCommunication.DoesNotExist:
            user_communication, is_created = CustomUserCommunication.objects.update_or_create(
                user=instance, defaults={"status": StatusChoices.ACTIVE.value}
            )
        ret["activity"] = user_communication.status
        return ret

    class Meta:
        model = CustomUser
        fields = ("id", "name", "surname", "phone", "email", "activity")


class CustomUserCommunicationSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели пользователя
    """

    class Meta:
        model = CustomUserCommunication
        fields = "__all__"


class CustomUserAvailableSerializer(serializers.Serializer):
    """
    Сериализатор метода available()
    """

    is_available = serializers.BooleanField(label="Доступен для коммуникации")
