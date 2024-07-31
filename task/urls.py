from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create),
    path('', views.index),
    path('delete', views.delete),
    path('update', views.update),
]