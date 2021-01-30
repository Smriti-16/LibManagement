"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URL conf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from new import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls, name='list'),
    path('index', views.index, name='home'),
    path('login_user', views.login_user, name='login_user'),
    path('logout_user', views.logout_user, name='logout_user'),
    path('logout_admin', views.logout_admin, name='logout_admin'),
    path('sign_up', views.signup, name='signup'),
    path('homepage_user', views.homepage_user, name='user_home'),
    path('login_admin', views.login_admin, name='login_admin'),
    path('homepage_admin', views.homepage_admin, name='admin_home'),
    path('add_book/', views.add_book, name='add_book'),
    path('update_book/<str:pk>/', views.update_book, name='update_book'),
    path('delete_book/<str:pk>/', views.delete_book, name='delete_book'),
    path('issue_book/', views.issue_book, name='issue_book'),
    path('user_status/', views.user_status, name='user_status'),
    path('return_book/<str:pk>/', views.return_book, name='return_book'),
    path('issue_user', views.issued_user, name='issued_user'),
    path('contact_view', views.contact_view, name='contact_view'),
]


urlpatterns += staticfiles_urlpatterns()