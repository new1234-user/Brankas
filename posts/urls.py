from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name="register"),
    path('login/', views.login_view, name="login"),
    path('dashboard/', views.dashboard_view, name="dashboard"),
    path('download/<int:brankas_id>/', views.download_brankas, name='download_brankas'),
    path("delete/<int:brankas_id>/", views.delete_brankas, name="delete_brankas"),
    path('brankas_list/semua/', views.brankas_list_view, name=('brankas_list'))
    ]
