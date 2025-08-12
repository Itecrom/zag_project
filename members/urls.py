from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('signup/', views.signup, name='signup'),
    path('members/', views.members_list, name='members_list'),
    path('members/new/', views.member_create, name='member_create'),
    path('members/<int:pk>/edit/', views.member_edit, name='member_edit'),
    path('export/csv/', views.export_members_csv, name='export_members_csv'),
]