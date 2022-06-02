from django.urls import path, include

from . import views

urlpatterns = [
    path('all_cases', views.TodoistListApiView.as_view()),
    path('case/<int:pk>', views.TodoOnceView.as_view()),
    path("cases/", views.TaskListCreateAPIView.as_view()),
    path("public_cases/", views.TodoPublicListApiView.as_view()),
]
