from django.contrib import admin


from .models import Todolist


@admin.register(Todolist)
class TodoListAdmin(admin.ModelAdmin):
    # вывод содержимого в листе админки
    list_display = ('title', 'important', 'public', 'status', 'create_at', 'update_at', 'author',)
    # поля только для чтения (неизменяемые поля при редактировании)
    readonly_fields = ('create_at',)
    # фильтры в админке
    list_filter = ('create_at', 'update_at', 'important', 'public', 'status',)





