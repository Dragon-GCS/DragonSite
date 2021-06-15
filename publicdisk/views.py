# Create your views here.
import os,mimetypes

from PIL import Image

from django.http import FileResponse
from django.shortcuts import render, redirect, get_object_or_404, reverse

from netdisk.models import File, Folder
from netdisk.utils import handle_upload_files, get_unique_folder_name, path_to_link, check_path_exits, remove_blank


def index(request):
    if request.method == "GET":
        Folder.create_public()
        return redirect(reverse("publicdisk:folder_show", kwargs={"path":"public"}))


def upload(request, path):
    if request.method == "POST":
        files = request.FILES.getlist("files")
        parent = get_object_or_404(Folder, path=path, owner=None)
        handle_upload_files(files, parent)
        # return render(request, 'pageJump.html', {'message':'上传成功'})


def download(request, path):
    if request.method == 'GET':
        name = os.path.basename(path)
        dir = os.path.dirname(path)
        file = get_object_or_404(File, name=name, dir__path=dir, owner=None)
        content_type, encoding = mimetypes.guess_type(str(file.get_file_path()))
        content_type = content_type or 'application/octet-stream'
        response = FileResponse(open(file.get_file_path(), 'rb'))
        response["Content-Length"] = file.size
        response['Content-Type'] = content_type
        response['Content-Disposition'] = f'attachment;filename="{name}"'
        if encoding:
            response["Content-Encoding"] = encoding
        return response


def preview(request,path):
    if request.method == 'GET':
        name = os.path.basename(path)
        dir = os.path.dirname(path)
        file = get_object_or_404(File, name=name, dir__path=dir, owner=None)
        cache_path = file.get_cache_path()

        check_path_exits(os.path.dirname(cache_path))

        if not os.path.isfile(cache_path):
            image = Image.open(file.get_file_path())
            image = image.resize((150, 150))
            image.save(cache_path)

        return FileResponse(open(cache_path, 'rb'))


def folder_show(request, path):
    if request.method == 'GET':
        if path == "":
            path = "root"
        basedir = get_object_or_404(Folder, path=path, owner=None)
        # 获取要展示的文件夹和文件
        folder = Folder.objects.filter(parent=basedir, owner=None)
        files = File.objects.filter(dir=basedir, owner=None)
        # 用于直接返回多层目录
        path_link = path_to_link(basedir)
        context = {'folders': folder, 'files': files, 'path': path, 'path_link': path_link}
        return render(request, "publicdisk/folder.html", context)


def create(request,path):
    if request.method == 'POST':
        parent = get_object_or_404(Folder, path=path, owner=None)
        name = remove_blank(request.POST.get("folder_name"))
        # 检查是否有重名
        folder_list = Folder.objects.filter(parent=parent, owner=None)
        unique_name = get_unique_folder_name(name, folder_list)
        # 创建文件夹
        path = "/".join([path, unique_name])
        Folder.objects.create(name=unique_name, path=path, parent=parent, owner=None)

        return redirect(reverse("publicdisk:folder_show", kwargs={"path":parent.path}))



def rename(request, type, path):
    if request.method == 'POST':
        new_name = remove_blank(request.POST.get("folder_name"))
        if type == 'folder':
            obj = Folder.objects.get(path=path,owner=None)
            folder_list = Folder.objects.filter(parent=obj.parent,owner=None)
            unique_name = get_unique_folder_name(new_name, folder_list)
            obj.name = unique_name
            obj.path = "/".join([os.path.dirname(path), unique_name])
            obj.save()
            message = "文件夹：{}重命名为{}".format(path, obj.path)

        elif type == 'file':
            name = os.path.basename(path)
            suffix = os.path.splitext(name)[1]
            dir = os.path.dirname(path)
            file = get_object_or_404(File, name=name, dir__path=dir, owner=None)
            if not os.path.splitext(new_name)[1]:
                new_name += suffix
            file_list = File.objects.filter(dir=file.dir)
            new_name = get_unique_folder_name(new_name, file_list)
            file.name = new_name
            file.save()
            message = "文件：{}重命名为{}".format(name, new_name)

        return render(request, 'pageJump.html', {'message':message})


def delete(request, type, path):
    if request.method == 'GET':
        if type =='folder':
            obj = Folder.objects.get(path=path,owner=None)
            obj.delete()    # 删除文件夹及其所有子文件夹与文件
            message = "文件夹：{}删除成功".format(path)
        elif type == 'file':
            name = os.path.basename(path)
            dir = os.path.dirname(path)
            file = get_object_or_404(File, name=name,dir__path=dir ,owner=None)
            file.delete()
            message = "文件：{} 删除成功".format(name)
        return render(request, 'pageJump.html', {'message':message})



def prev_folder(request):
    if request.method == 'GET':
        back_path = os.path.dirname(request.META.get('HTTP_REFERER'))
        return redirect(back_path)