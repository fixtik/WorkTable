from django.urls import path, include

from . import views

urlpatterns = [
    path('all_cases', views.TodoistListApiView.as_view()),
    path('case/<int:pk>', views.TodoOnceView.as_view()),
]
