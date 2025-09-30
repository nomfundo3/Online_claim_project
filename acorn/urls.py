"""acorn URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from system_management import views
from django.contrib.auth import views as auth_views
from django.conf import settings


urlpatterns = [
    path('', views.login_view, name='login'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/login/home/', views.redirect_user, name='redirect_user'),

    path('system_management/', include('system_management.urls')),
    path('system_management_api/', include('system_management.api.urls')),

    path('claims/', include('claims.urls')),
    path('claims_api/', include('claims.api.urls')),

    path('surveys/', include('surveys.urls')),
    path('surveys_api/', include('surveys.api.urls')),

    path('application/', include('application.urls')),
    path('application_api/', include('application.api.urls')),

    path('password_reset/', auth_views.PasswordResetView.as_view(
        html_email_template_name='registration/password_reset_email.html'
    ), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
]
