# coding = utf-8
# Dragon's Python3.8 code
# Created at 2021/5/6 19:49
# Edit with PyCharm

from django.urls import path,re_path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'netdisk'
urlpatterns = [
    re_path(r'^$', views.index),
    re_path(r'^home/$', views.index),
    path('create/', views.create_folder),
    path('back/', views.back_folder),
    path('upload_file/', views.upload_file),
    re_path(r'^delete/(?P<path>(\w+/?)*)$', views.delete_folder),
    re_path(r'^folder/(?P<path>(\w+/?)*)$', views.folder_show),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)