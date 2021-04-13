# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import RegistrationView,ProfileView

app_name = 'users'

urlpatterns = [
    # url(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
            path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
            path('logout/',LogoutView.as_view(next_page="/"), name='logout'),
                path('registration/',RegistrationView.as_view(), name='register'),
                path('profile/',ProfileView.as_view(),name='profile')
]
