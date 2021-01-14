from django.contrib import admin
from .models import NewUserTodo


class NewUserTodoAdmin(admin.ModelAdmin):
    list_display = "user title created date_completed important".split()
    list_filter = "created important date_completed".split()
    editable_fields = ("important",)
    readonly_fields = ("created",)


admin.site.register(NewUserTodo, NewUserTodoAdmin)
