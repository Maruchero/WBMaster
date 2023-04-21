from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="index"),
    path("docs/", views.docs, name="docs"),
    path("logout/", views.logout, name="logout"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("projects/add/", views.add_project, name="add_project"),
    # path("projects/<int>", views.project, name="project_details"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
