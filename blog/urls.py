from django.urls import path
from .views import post_list, post_create, post_detail

urlpatterns = [
    path('', post_list, name='post_list'),
    path('create/', post_create, name='post_create'),
    path('post/<int:post_id>/', post_detail, name='post_detail'),
    
]