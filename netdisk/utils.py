# coding = utf-8
# Dragon's Python3.8 code
# Created at 2021/5/8 21:50
# Edit with PyCharm

import hashlib
import os
import shutil
import uuid

from django.conf import settings

from .models import File, Link

MEDIA_ROOT = os.path.join(settings.MEDIA_ROOT,'netdisk')

def check_path(path):
    if not os.path.isdir(path):
        os.mkdir(path)


def handle_upload_files(files, parent, owner=None):
    # 获取当前目录内的文件
    file_list = File.objects.filter(dir=parent,owner=owner)
    # 检查目录是否存在
    check_path(MEDIA_ROOT)

    for file in files:
        digest = hashlib.md5()
        # 防止文件重名
        unique_name = get_unique_file_name(file.name, file_list)
        temp_name = os.path.join(MEDIA_ROOT, str(uuid.uuid1()))
        ## 计算文件的MD5并作为文件名保存至MEDIA文件夹
        with open(temp_name, 'wb+') as destination:
            for chunk in file.chunks(chunk_size=1024):
                destination.write(chunk)
                destination.flush()
                digest.update(chunk)

        digest = digest.hexdigest()
        file_path = os.path.join(MEDIA_ROOT, digest)
        # 创建文件对象
        file = File.objects.create(name=unique_name,
                                   dir=parent,
                                   owner=owner,
                                   digest=digest,
                                   size=file.size)
        # 增加对应的文件链接
        Link.add_link(file)
        # 重命名文件
        shutil.move(temp_name,file_path)


def get_unique_folder_name(name, content_list):
    ## 检查是否有重名的文件夹并按顺序生成新名称
    folder_list = [content.name for content in content_list]
    if name in folder_list:
        cont = 1
        while f'{name}({cont})' in folder_list:
            cont += 1
        name = f'{name}({cont})'
    return name


def get_unique_file_name(name, content_list):
    ## 检查是否有重名的文件夹并按顺序生成新名称
    prefix, suffix = os.path.splitext(name)
    folder_list = [content.name for content in content_list]
    if name in folder_list:
        cont = 1
        while f'{prefix}({cont}){suffix}' in folder_list:
            cont += 1
        name = f'{prefix}({cont}){suffix}'
    return name


def path_to_link(folder):
    path_link = []
    while folder.parent:
        path_link.append(("/"+folder.name, folder.path))
        folder = folder.parent
    path_link.append((folder.name,folder.path))
    return reversed(path_link)
