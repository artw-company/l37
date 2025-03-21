from departments.models import Department, DepartmentCommunication
from rest_framework import serializers


class DepartmentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для подразделений
    """

    class Meta:
        model = Department
        fields = "__all__"


class DepartmentCommunicationSerializer(serializers.ModelSerializer):
    """
    Сериализатор для правил коммуникации
    """

    class Meta:
        model = DepartmentCommunication
        fields = "__all__"
