# Create your views here.
import os,mimetypes

from PIL import Image

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, FileResponse
from django.shortcuts import render, redirect, get_object_or_404, reverse

from .models import File, Folder, Link
from .utils import handle_upload_files, get_unique_folder_name, path_to_link


@login_required
def index(request):
    if request.method == "GET":
        Folder.create_root(request.user)
        return redirect(reverse("netdisk:folder_show", kwargs={"path":"root"}))

@login_required
def upload(request, path):
    if request.method == "POST":
        files = request.FILES.getlist("files")
        parent = get_object_or_404(Folder, path=path, owner=request.user)
        handle_upload_files(files, parent, request.user)
        return render(request, 'pageJump.html', {'message':'上传成功'})

@login_required
def download(request, path):
    if request.method == 'GET':
        name = os.path.basename(path)
        dir = os.path.dirname(path)
        file = get_object_or_404(File, name=name, dir__path=dir,owner=request.user)
        content_type, encoding = mimetypes.guess_type(str(file.get_file_path()))
        content_type = content_type or 'application/octet-stream'
        response = FileResponse(open(file.get_file_path(), 'rb'))
        response["Content-Length"] = file.size
        response['Content-Type'] = content_type
        response['Content-Disposition'] = f'attachment;filename="{name}"'
        if encoding:
            response["Content-Encoding"] = encoding
        return response

@login_required
def preview(request,path):
    if request.method == 'GET':
        name = os.path.basename(path)
        dir = os.path.dirname(path)
        file = get_object_or_404(File, name=name, dir__path=dir, owner=request.user)
        cache_path = file.get_cache_path()
        if not os.path.isdir(os.path.dirname(cache_path)):
            os.mkdir(os.path.dirname(cache_path))
        if not os.path.isfile(cache_path):
            image = Image.open(file.get_file_path())
            image = image.resize((150,150))
            image.save(cache_path)
        return FileResponse(open(cache_path,'rb'))

@login_required
def folder_show(request, path):
    if request.method == 'GET':
        if path == "":
            path = "root"
        basedir = get_object_or_404(Folder, path=path, owner=request.user)
        folder = Folder.objects.filter(parent=basedir, owner=request.user)
        files = File.objects.filter(dir=basedir, owner=request.user)
        path_link = path_to_link(basedir)   # 用于直接返回多层目录
        context = {'folders': folder, 'files': files, 'path':path,'path_link':path_link}
        return render(request, "netdisk/folder.html", context)

@login_required
def create(request,path):
    if request.method == 'POST':
        parent = get_object_or_404(Folder, path=path, owner=request.user)
        name = request.POST.get("folder_name")
        folder_list = Folder.objects.filter(parent=parent,owner=request.user)
        unique_name = get_unique_folder_name(name, folder_list)
        path = "/".join([path, unique_name])
        Folder.objects.create(name=unique_name, path=path, parent=parent, owner=request.user)
        return redirect(reverse("netdisk:folder_show", kwargs={"path":parent.path}))


@login_required
def rename(request, type, path):
    if request.method == 'POST':
        if type == 'folder':
            obj = Folder.objects.get(path=path,owner=request.user)
            name = request.POST.get("new_name")
            if obj.name != name:
                folder_list = Folder.objects.filter(parent=obj.parent,owner=request.user)
                unique_name = get_unique_folder_name(name, folder_list)
                obj.name = unique_name
                obj.path = "/".join([os.path.dirname(path), unique_name])
                obj.save()
            message = "文件夹：{}重命名为{}".format(path, obj.path)

        elif type == 'file':
            name = os.path.basename(path)
            new_name = request.POST.get("new_name")
            if new_name != name:
                suffix = os.path.splitext(name)[1]
                dir = os.path.dirname(path)
                file = get_object_or_404(File, name=name, dir__path=dir, owner=request.user)

                if not os.path.splitext(new_name)[1]:
                    new_name += suffix

                file_list = File.objects.filter(dir=file.dir)
                new_name = get_unique_folder_name(new_name, file_list)
                file.name = new_name
                file.save()
                message = "文件：{}重命名为{}".format(name, new_name)

        return render(request, 'pageJump.html', {'message':message})

@login_required
def delete(request, type, path):
    if request.method == 'GET':
        if type =='folder':
            obj = Folder.objects.get(path=path,owner=request.user)
            obj.remove()    # 删除文件夹及其所有子文件夹与文件
            message = "文件夹：{}删除成功".format(path)
        elif type == 'file':
            name = os.path.basename(path)
            dir = os.path.dirname(path)
            file = get_object_or_404(File, name=name,dir__path=dir ,owner=request.user)
            # 使用Link.minus_link删除一条连接以对应的一条文件数据
            Link.minus_link(file)
            message = "文件：{} 删除成功".format(name)
        return render(request, 'pageJump.html', {'message':message})


@login_required
def prev_folder(request):
    if request.method == 'GET':
        back_path = os.path.dirname(request.META.get('HTTP_REFERER'))
        return redirect(back_path)