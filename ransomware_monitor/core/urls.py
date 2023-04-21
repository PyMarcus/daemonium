from django.urls import path, include
from .views import IndexView
from django.contrib.auth.views import LoginView


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
]
