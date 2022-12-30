from django.contrib import admin
from .models import FaceVector


class FaceVectorAdmin(admin.ModelAdmin):

    list_display = [
        "name",
        "created_at",
    ]


admin.site.register(FaceVector, FaceVectorAdmin)
