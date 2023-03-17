from django import shortcuts
from . import views
from django.urls import path



urlpatterns = [ 
    path('login', views.login_page, name = 'login'),
    path('logout', views.logout_page, name = 'logout'),
    path('', views.profiles, name = 'profiles'),
    path("register", views.register_user, name = 'register'),
    path('user_profile/<str:pk>', views.user_profile, name = 'user_profile'),
    path('account', views.user_account, name="account"),
    path('edit_profile', views.edit_profile, name="edit_profile"),
    path('create_skill', views.create_skill, name="create_skill"),
    path('update_skill/<str:pk>', views.update_skill, name="update_skill"),
    path('delete_skill/<str:pk>', views.delete_skill, name="delete_skill"),
    path('inbox', views.inbox, name="inbox"),
    path('message/<str:pk>/', views.viewMessage, name="message")

]