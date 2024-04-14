from django.urls import path

from chat import views

urlpatterns = [
    path("", views.ChatAPIView.as_view()),
    path("messages/", views.MessageAPIView.as_view()),
]
