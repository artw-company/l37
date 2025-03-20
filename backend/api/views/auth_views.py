from api.serializers import LogInResponseSerializer, LogInSerializer
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework_simplejwt.views import TokenObtainPairView


@extend_schema_view(
    post=extend_schema(
        summary="Аутентификация клиента API.",
        description="Метод для аутентификации клиента API.",
        responses={200: LogInResponseSerializer},
    ),
)
class LogInView(TokenObtainPairView):
    serializer_class = LogInSerializer
