from api.permissions import ClientPermissions
from api.serializers.auth_serializer import ClientSerializer
from api.serializers.client_serializers import ClientCreateSerializer
from common.constants import StatusChoices
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics, mixins, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated


@extend_schema_view(
    list=extend_schema(
        request=None,
        summary="Получение списка активных клиентов API.",
        description="Клиенты имеют доступ к методам API.",
    ),
    retrieve=extend_schema(
        summary="Получение клиента по id.",
    ),
    update=extend_schema(
        summary="Изменение клиента API. Все поля.",
    ),
    partial_update=extend_schema(
        summary="Изменение клиента API по id. Только переданные поля.",
    ),
)
class ClientViewSet(
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = ClientSerializer
    queryset = get_user_model().objects.filter(status=StatusChoices.ACTIVE)
    permission_classes = (
        IsAuthenticated,
        ClientPermissions,
    )


@extend_schema_view(
    post=extend_schema(
        summary="Создание нового клиента API.",
        description="Метод создания нового клиента API.",
    ),
)
class SignUpView(generics.CreateAPIView):
    serializer_class = ClientCreateSerializer
    queryset = get_user_model().objects.all()
    permission_classes = (AllowAny,)
