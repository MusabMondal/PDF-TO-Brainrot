from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home2/', views.home2, name='home2'),
    path('file_upload/', views.file_upload, name='file_upload'),
]