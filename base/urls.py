from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path("docs/", views.docs, name="docs"),
    path("logout/", views.logout, name="logout"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("dashboard/", views.dashboard, name="dashboard"),
]
