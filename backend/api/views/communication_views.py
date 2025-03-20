from datetime import datetime as dt

from api.serializers.comminication_serializers import (
    CommunicationBookingSerializer,
    CommunicationKindSerializer,
    CommunicationSerializer,
    CommunicationSourceSerializer,
    CommunicationStatusUpdateSerializer,
)
from common.constants import CommunicationStatusChoices, StatusChoices
from communications.models import Communication, CommunicationKind, CommunicationSource
from departments.models import DepartmentCommunication
from django.db.models import Sum
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from users.models import CustomUser


@extend_schema_view(
    list=extend_schema(
        request=None,
        summary="Получение списка активных типов коммуникаций.",
    ),
    create=extend_schema(
        summary="Создание типа коммуникации",
    ),
)
class CommunicationKindViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = CommunicationKindSerializer
    queryset = CommunicationKind.objects.filter(status=StatusChoices.ACTIVE)


@extend_schema_view(
    list=extend_schema(
        request=None,
        summary="Получение списка активных каналов коммуникаций.",
    ),
    create=extend_schema(
        summary="Создание канала коммуникации.",
    ),
)
class CommunicationSourceViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = CommunicationSourceSerializer
    queryset = CommunicationSource.objects.filter(status=StatusChoices.ACTIVE)


@extend_schema_view(
    list=extend_schema(
        request=None,
        summary="Получение списка активных каналов коммуникаций.",
    ),
    create=extend_schema(
        summary="Отправка коммуникации",
        description=(
            """
                При отправке (создании) коммуникации, учитывается количество коммуникаций
                пользователя в департаменте в единицу времени и доступность пользователя для коммуникации.
                В случае превышения лимита или недоступности пользователя, статус коммуникации 'не отправлено'.
                Для дальнейшей обработки таких коммуникаций можно использовать периодические асинхронные задачи.
                Пример даты: "2025-03-19T16:03:15.153Z"
                """
        ),
    ),
    update=extend_schema(summary="Обновление коммуникации по id."),
    partial_update=extend_schema(
        summary="Изменение коммуникации по id. Только переданные поля.",
    ),
)
class CommunicationViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = CommunicationSerializer
    queryset = Communication.objects.all()

    def create(self, request, *args, **kwargs):
        data = self.request.data

        # Проверка доступности клиента
        user = CustomUser.objects.filter(pk=data.get("user")).first()

        is_available = user.user_communications.filter(
            status=StatusChoices.ACTIVE.value,
        ).exists()

        # Проверка департамента
        department_id = data.get("department")
        department_queryset = DepartmentCommunication.objects.filter(department_id=department_id)
        base_limit_rate = department_queryset.first().limit_per_unit
        amount_current_limit_rate = (
            department_queryset.annotate_current_limit_rate().aggregate(amount_limit_rate=Sum("current_limit_rate"))
        ).get("amount_limit_rate") or 0
        if (base_limit_rate and base_limit_rate < amount_current_limit_rate) or not is_available:
            data.update(status=CommunicationStatusChoices.FAILED)
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=CommunicationBookingSerializer,
        summary="Создание отложенной коммуникации",
        description=(
            """
                Отложенная коммуникация имеет будущее время и создается со статусом 'забронировано'.
                Если время текущее, возвращает ошибку. Пример даты: "2025-03-19T16:03:15.153Z"
                """
        ),
    )
    @action(detail=False, methods=["post"], url_path="booking")
    def booking(self, request):
        data: dict = self.request.data
        date = dt.strptime(data.get("communication_date"), "%Y-%m-%dT%H:%M:%S.%fZ")
        if date >= dt.now():
            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        return Response({"communication_date": ["Дата не находится в будущем"]}, status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=CommunicationStatusUpdateSerializer,
        summary="Обновление статуса коммуникации",
        description=(
            """
                Обновляет communication_status на 'delivered' или 'viewed'.
                """
        ),
    )
    @action(detail=True, methods=["patch"], url_path="update_status")
    def update_status(self, request, pk=None):
        communication: Communication = self.get_object()
        if communication.status != CommunicationStatusChoices.FAILED.value:
            serializer = CommunicationStatusUpdateSerializer(communication, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": ["Коммуникация не была отправлена"]}, status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        if self.action == "booking":
            return CommunicationBookingSerializer
        return CommunicationSerializer
