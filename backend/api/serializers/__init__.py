from .auth_serializer import LogInResponseSerializer, LogInSerializer
from .client_serializers import ClientCreateSerializer, ClientSerializer
from .comminication_serializers import (
    CommunicationBookingSerializer,
    CommunicationKindSerializer,
    CommunicationSerializer,
    CommunicationSourceSerializer,
)
from .custom_user_serializers import (
    CustomCreateUserSerializer,
    CustomUserAvailableSerializer,
    CustomUserCommunicationSerializer,
    CustomUserSerializer,
)
from .department_serializers import (
    DepartmentCommunicationSerializer,
    DepartmentSerializer,
)
