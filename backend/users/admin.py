from django.contrib import admin

from users.models import CustomUser, CustomUserCommunication


# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    ...


@admin.register(CustomUserCommunication)
class CustomUserAdmin(admin.ModelAdmin):
    ...
