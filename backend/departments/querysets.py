from common.constants import CommunicationStatusChoices
from django.db.models import Count, F, OuterRef, QuerySet, Subquery
from django.db.models.functions import Trunc


class DepartmentCommunicationQuerySet(QuerySet):

    def annotate_current_limit_rate(self):
        from communications.models import Communication

        current_limit_rate = Subquery(
            Communication.objects.filter(
                user_id=OuterRef("department__communications__user"),
                department_id=OuterRef("department"),
                status=CommunicationStatusChoices.SEND,
            )
            .annotate(hour=Trunc("communication_date", kind=F("unit")))
            .annotate(count=Count("id"))
            .values("count")[:1]
        )
        return self.annotate(current_limit_rate=current_limit_rate)
