from django.contrib import admin

from communications.models.communications import FavoriteSource, Communication, CommunicationKind, CommunicationSource


# Register your models here.
@admin.register(Communication)
class ModelNameAdmin(admin.ModelAdmin):
    ...


@admin.register(FavoriteSource)
class ModelNameAdmin(admin.ModelAdmin):
    ...


@admin.register(CommunicationKind)
class ModelNameAdmin(admin.ModelAdmin):
    ...


@admin.register(CommunicationSource)
class ModelNameAdmin(admin.ModelAdmin):
    ...
