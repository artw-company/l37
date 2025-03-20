from django_filters import CharFilter, FilterSet
from users.models import CustomUser


class CustomUserFilterSet(FilterSet):
    email = CharFilter(lookup_expr="iexact")
    name = CharFilter(lookup_expr="icontains")

    class Meta:
        model = CustomUser
        fields = (
            "email",
            "name",
        )
