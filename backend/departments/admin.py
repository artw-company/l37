from django.contrib import admin

from departments.models import DepartmentCommunication, Department


# Register your models here.
@admin.register(Department)
class ModelNameAdmin(admin.ModelAdmin):
    ...


@admin.register(DepartmentCommunication)
class ModelNameAdmin(admin.ModelAdmin):
    ...
