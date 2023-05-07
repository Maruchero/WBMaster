from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="index"),
    path("logout/", views.logout, name="logout"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("projects/add/", views.add_project, name="add_project"),
    path("projects/<str:pk>/", views.project, name="project_details"),
    path("projects/edit/<str:pk>/", views.edit_project, name="edit_project"),
    path("projects/delete/<str:pk>/", views.delete_project, name="delete_project"),
    path("tasks/add/", views.add_task, name="add_task"),
    path("tasks/edit/<str:pk>/", views.edit_task, name="edit_task"),
    path("tasks/delete/<str:pk>/", views.delete_task, name="delete_task"),
    path("docs/", views.docs, name="docs"),
    path("docs/django/", views.docs, name="docs_django"),
    path("docs/models/", views.docs_models, name="docs_models"),
    path("docs/urls/", views.docs, name="docs_urls"),
    path("docs/views/", views.docs, name="docs_views"),
    path("docs/templates/", views.docs, name="docs_templates"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
