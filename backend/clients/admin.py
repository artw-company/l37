from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from clients.models import Client


@admin.register(Client)
class ModelNameAdmin(UserAdmin):
    additional_fields = ("status",)

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        fields.append('status')

    def get_fieldsets(self, request, obj=None):
        field_set = super().get_fieldsets(request, obj)
        print(field_set)
        field_set = list(field_set)
        field_set.append(("Дополнительные поля", {"fields": self.additional_fields}))
        return field_set
