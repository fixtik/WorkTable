from rest_framework.permissions import BasePermission, SAFE_METHODS

class OnlyAuthorEditTask(BasePermission):
    """Запрет на редактирование не автора
      и доступ для чтения непубличных записей"""
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            if obj.public:
                return True
            else:
                return request.user == obj.author
        return request.user == obj.author