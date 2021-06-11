import filetype
import os

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

MEDIA_ROOT = os.path.join(settings.MEDIA_ROOT,'netdisk')

class File(models.Model):
    name = models.CharField('文件名',max_length=256)
    owner = models.ForeignKey(User, on_delete=models.CASCADE,null=True,default=None)
    dir = models.ForeignKey('Folder', on_delete=models.CASCADE, null=False)
    digest = models.ForeignKey('Digest', on_delete=models.CASCADE, null=False)
    size = models.IntegerField(default=0)
    upload_time = models.DateField(auto_now_add=True)
    is_image_file = ''

    def __str__(self):
        return self.get_url_path()

    def show_name(self):
        filename, suffix = os.path.splitext(self.name)
        if len(filename) > 10:
            return f"{filename[:10]}…{suffix}"
        return self.name
        
    def get_url_path(self):
        return '/'.join([self.dir.path, self.name])

    def get_cache_path(self):
        return os.path.join(settings.CACHE_PATH, self.digest.digest + settings.IMAGE_CACHE_TYPE)

    def get_file_path(self):
        return os.path.join(MEDIA_ROOT, self.digest.digest)

    def remove_file(self):
        os.remove(self.get_file_path())

    def is_image(self):
        return filetype.image_match(self.get_file_path())

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
    path = models.CharField('文件夹路径', max_length=2048)
    parent = models.ForeignKey('Folder',null=True,on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)
    creat_time = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.path

    def show_name(self):
        if len(self.name) > 10:
            return self.name[:10] + "…"
        return self.name

    @classmethod
    def create_root(cls, owner):
        if not cls.objects.filter(path='root', owner=owner):
            cls.objects.create(name='root', path='root', parent=None, owner=owner)

    @classmethod
    def create_public(cls):
        if not cls.objects.filter(path='public'):
            cls.objects.create(name='public', path='public', parent=None)





class Digest(models.Model):
    digest = models.CharField(max_length=32, primary_key=True)  # 记录文件的md5

    def __str__(self):
        return f"{self.digest}: {list(self.file_set.values_list('name'))}"

    def get_md5_path(self):
        return os.path.join(MEDIA_ROOT, self.digest)

    def check_digest(self):
        if not os.path.isfile(self.get_md5_path()):
            self.delete()
            print(f"digest'{self.digest}'无对应md5文件，已删除")
        elif not self.file_set.all():
            os.remove(self.get_md5_path())
            self.delete()
            print(f"digest'{self.digest}'无对应文件记录，已删除")

    @classmethod
    def digest_repair(cls):
        if not os.path.isdir(MEDIA_ROOT):
            os.makedirs(MEDIA_ROOT)
        # 用于清除没有对应记录的文件
        for file in os.listdir(MEDIA_ROOT):
            if not cls.objects.filter(digest=file):
                print(f"文件'{file}'无对应digest记录，已删除")
                os.remove(os.path.join(MEDIA_ROOT, file))
        # 用于清除没有文件记录或没有对应文件的digest
        for digest in cls.objects.all():
            digest.check_digest()