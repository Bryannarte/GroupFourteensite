from django.urls import path
from . import views

urlpatterns = [
    path('gender/list', views.gender_list),
    path('gender/add', views.add_gender),
    path('gender/edit/<int:genderId>', views.edit_gender),
    path('gender/delete/<int:genderId>', views.delete_gender),
    path('user/list', views.user_list),
    path('user/add', views.add_user),
    path('user/edit/<int:userId>', views.edit_user),
    path('user/delete/<int:userId>', views.delete_user),
    path('login', views.user_login),
    path('logout', views.user_logout)
]
