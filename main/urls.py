from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get-file-content/', views.get_file_content, name='get_file_content'),
]
