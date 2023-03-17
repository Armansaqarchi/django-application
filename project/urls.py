from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from . import views
from django.conf import settings
#this method down here is gonna help us create a url for our static files
from django.conf.urls.static import static


urlpatterns = [
    path("project/<str:pk>", views.project, name = "project"),
    path("projects/", views.projects, name = "projects"),
    path("create_project/",views.create_project, name = "create_project"),
    path("update_project/<str:pk>/", views.update_project, name = "update_project"),
    path("delete_project/<str:pk>/", views.delete_project, name = "delete_project"),
    path("create_project/<str:pk>/", views.create_project, name = "create_project")
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)

