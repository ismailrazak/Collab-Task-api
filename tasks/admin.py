from django.contrib import admin

from .models import Attachment, Task, TaskList

admin.site.register(Task, admin.ModelAdmin)
admin.site.register(TaskList)
admin.site.register(Attachment)
