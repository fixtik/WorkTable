from django.contrib import admin


from .models import Todolist


@admin.register(Todolist)
class TodoListAdmin(admin.ModelAdmin):
    list_display = ('title', 'important', 'public', 'status', 'create_at', 'update_at')

    readonly_fields = ('create_at',)





