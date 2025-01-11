from django.contrib import admin

from .models import House


class CustomHouseModelAdmin(admin.ModelAdmin):
    readonly_fields = [
        "points",
        "completed_tasks_count",
        "not_completed_tasks_count",
        "id",
        "created_on",
    ]


admin.site.register(House, CustomHouseModelAdmin)
