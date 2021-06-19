# coding = utf-8
# Dragon's Python3.8 code
# Created at 2021/6/9 20:02
# Edit with PyCharm

from django.urls import re_path

from . import views

app_name = 'publicdisk'
urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'back/$', views.prev_folder, name='prev_folder'),
    re_path(r'^create/(?P<path>(\S+/?)*)$', views.create, name='create'),
    re_path(r'^upload/(?P<path>(\S+/?)*)$', views.upload, name='upload'),
    re_path(r'^preview/(?P<path>([\S]+/?)*)$', views.preview, name='preview'),
    re_path(r'^download/(?P<path>(\S+/?)*)$', views.download, name='download'),
    re_path(r'^folder/(?P<path>([\S]+/?)*)$', views.folder_show, name='folder_show'),
    re_path(r'^delete/(?P<type>(file|folder))&(?P<path>([\S]+/?)*)$', views.delete, name='delete'),
    re_path(r'^rename/(?P<type>(file|folder))&(?P<path>([\S]+/?)*)$', views.rename, name='rename'),
]