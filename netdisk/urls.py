# coding = utf-8
# Dragon's Python3.8 code
# Created at 2021/5/6 19:49
# Edit with PyCharm

from django.urls import re_path
from . import views
from django.conf.urls.static import static
from django.conf import settings


app_name = 'netdisk'
urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'back/$', views.prev_folder, name='prev_folder'),
    re_path(r'^create/(?P<path>(\S+/?)*)$', views.create, name='create'),
    re_path(r'^upload/(?P<path>(\S+/?)*)$', views.upload, name='upload'),
    re_path(r'^download/(?P<path>(\S+/?)*)$', views.download, name='download'),
    re_path(r'^folder/(?P<path>([\S]+/?)*)$', views.folder_show, name='folder_show'),
    re_path(r'^delete/(?P<type>(file|folder))&(?P<path>([\S]+/?)*)$', views.delete, name='delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

