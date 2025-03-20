from api.filters import CustomUserFilterSet
from api.serializers import (
    CustomCreateUserSerializer,
    CustomUserAvailableSerializer,
    CustomUserSerializer,
)
from common.constants import StatusChoices
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from users.models import CustomUser


@extend_schema_view(
    list=extend_schema(
        summary="Получение списка пользователей.",
    ),
    retrieve=extend_schema(
        summary="Получение пользователя по id.",
    ),
    create=extend_schema(
        summary="Создание пользователя.",
        description="""Создает пользователя в статусе готовности, переданном в поле activity: active / blocked""",
    ),
    update=extend_schema(
        summary="Изменение пользователя по id. Все поля.",
    ),
    partial_update=extend_schema(
        summary="Изменение пользователя по id. Только переданные поля.",
    ),
    destroy=extend_schema(
        summary="Удаление пользователя по id. Все поля.",
    ),
)
class CustomUserViewSet(viewsets.ModelViewSet):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    filterset_class = CustomUserFilterSet

    def get_serializer_class(self):
        result = CustomUserSerializer
        if self.action == "available":
            result = CustomUserAvailableSerializer
        elif self.action == "create":
            result = CustomCreateUserSerializer
        return result

    @extend_schema(
        summary="Получение доступных для коммуникации Пользователей",
        description="""Возвращает список Пользователей, доступных для коммуникации в данный момент""",
        responses={200: CustomUserSerializer(many=True)},
    )
    @action(detail=False)
    def active_users(self, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(
            user_communications__status=StatusChoices.ACTIVE.value,
        ).distinct()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Проверяет пользователя на доступность для коммуникаций",
        description="""Получает id пользователя, возвращает True если данный пользователь доступен для коммуникации
         и False в противном случае""",
        request=None,
        responses={200: CustomUserAvailableSerializer},
    )
    @action(detail=True)
    def available(self, request, pk=None):
        user = self.get_object()  # Получаем конкретного пользователя по pk
        is_available = user.user_communications.filter(
            status=StatusChoices.ACTIVE.value,
        ).exists()
        data = {"is_available": is_available}
        serializer = self.get_serializer(data=data)
        serializer.is_valid()
        return Response(serializer.data, status=status.HTTP_200_OK)
