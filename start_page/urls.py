from django.urls import path, include
from . import views

urlpatterns = [
    path('start_page', views.IndexView.as_view()),
]