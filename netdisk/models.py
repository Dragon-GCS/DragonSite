from django.db import models
from django.conf import settings
#from django.contrib.auth.models import User

import os
# Create your models here.

MEDIA_ROOT = settings.MEDIA_ROOT

class File(models.Model):
    name = models.CharField('文件名',max_length=256)
    #owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    dir = models.ForeignKey('Folder', on_delete=models.CASCADE, null=False)
    digest = models.CharField(max_length=32)
    size = models.IntegerField(default=0)
    upload_time = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_url_path(self):
        return '/'.join([self.dir.path, self.name])

    def get_file_path(self):
        return os.path.join(MEDIA_ROOT, self.digest)

    def remove_file(self):
        os.remove(self.get_file_path())

    def get_file_size(self):
        size = self.size
        if size > 1024 ** 3:  # GB
            size = '{:.2f} GB'.format(size / (1024 ** 3))
        elif size > 1024 ** 2:  # MG
            size = '{:.2f} MB'.format(size / (1024 ** 2))
        elif size > 1024:
            size = '{:.2f} KB'.format(size / (1024))
        else:
            size = '{:.2f} Bytes'.format(size)
        return size


class Folder(models.Model):
    name = models.CharField('文件夹名称', max_length=32)
    path = models.CharField('文件夹路径', unique=True, max_length=2048)
    parent = models.ForeignKey('Folder',to_field='path',null=True,on_delete=models.CASCADE)
    creat_time = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.path

    @classmethod
    def create_root(cls):
        if not cls.objects.filter(path='root'):
            return cls.objects.create(name='root',path='root',parent=None)

    def remove(self):
        for subdir in Folder.objects.filter(parent=self.path):
            for file in subdir.file_set.all():
                Link.minus_link(file)

        for file in self.file_set.all():
            Link.minus_link(file)

        self.delete()




class Link(models.Model):
    digest = models.CharField(max_length=32, primary_key=True)  # 记录文件的md5
    links = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.digest}: {self.get_all_link()}"

    @classmethod
    def add_link(cls,file):
        objs, created = cls.objects.get_or_create(digest=file.digest)
        objs.links += 1
        objs.save()

    @classmethod
    def minus_link(cls, file):
        objs = cls.objects.get(digest=file.digest)
        objs.links -= 1

        if objs.links == 0:
            file.remove_file()
            objs.delete()
        else:
            objs.save()

        file.delete()

    def get_all_link(self):
        list = [file.name for file in File.objects.filter(digest=self.digest)]
        return list