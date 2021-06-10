"""DragonSite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf import settings


def index(request):
    return render(request, 'base.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index),
    path('netdisk/', include('netdisk.urls')),
    path('publicdisk/', include('publicdisk.urls')),
    path('login/',include('login.urls')),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}, name='static'),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),
]
'''
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
仅在DEBUG=TRUE 能够提供静态文件服务
文档上说上面re_path也仅在DEBUG环境生效，然而并不是
'''

