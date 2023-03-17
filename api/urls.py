from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("", views.getRoutes, name="api"),
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("projects", views.getProjects, name="projects"),
    path("project/<str:pk>", views.getProject, name="project"),
    path("project/<str:pk>/vote/", views.vote_project, name="vote_project")
]