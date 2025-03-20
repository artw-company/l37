from api.serializers.department_serializers import (
    DepartmentCommunicationSerializer,
    DepartmentSerializer,
)
from departments.models import Department, DepartmentCommunication
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins, viewsets


@extend_schema_view(
    list=extend_schema(
        summary="Получение списка департаментов.",
    ),
    create=extend_schema(
        summary="Создание департамента.",
    ),
)
class DepartmentViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):

    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()


@extend_schema_view(
    list=extend_schema(
        summary="Получение списка правил для коммуникации для департамента.",
        description="Возвращает список правил коммуникации для департамента.",
    ),
    create=extend_schema(
        summary="Создание правил коммуникации для департамента.",
        description=(
            """Cоздает правило коммуникации для департамента.
                   Возможные значения для поля unit: hour, minute, second"""
        ),
    ),
)
class DepartmentCommunicationViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):

    serializer_class = DepartmentCommunicationSerializer
    queryset = DepartmentCommunication.objects.all()
