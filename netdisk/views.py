# Create your views here.
from django.shortcuts import render,redirect,get_object_or_404,reverse
from django.http import HttpResponse
from .models import File, Folder, Link
from django.utils.http import urlunquote
import os,cv2,numpy
from django.contrib.auth.decorators import login_required
from .utils import handle_upload_files, get_unique_folder_name,path_to_link



@login_required
def index(request):
    if request.method == "GET":
        return render(request, 'netdisk/base.html')

@login_required
def upload(request, path):
    if request.method == "POST":
        files = request.FILES.getlist("files")
        parent = get_object_or_404(Folder, path=path)
        if not files:
            return render(request, 'netdisk/pageJump.html', {'message':'请选择文件'})
        else:
            handle_upload_files(files, parent)
            return render(request, 'netdisk/pageJump.html', {'message':'上传成功'})

@login_required
def download(request, path):
    if request.method == 'GET':
        name = os.path.basename(path)
        dir = os.path.dirname(path)
        file = get_object_or_404(File, name=name, dir__path=dir)
        content = open(file.get_file_path(), 'rb')
        response = HttpResponse(content)
        response["Content-Length"] = file.size
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = f'attachment;filename="{name}"'
        return response

@login_required
def preview(request,path):
    if request.method == 'GET':
        name = os.path.basename(path)
        dir = os.path.dirname(path)
        file = get_object_or_404(File, name=name, dir__path=dir)
        cache_path = file.get_cache_path()
        if not os.path.isdir(os.path.dirname(cache_path)):
            os.mkdir(os.path.dirname(cache_path))
        if not os.path.isfile(cache_path):
            image = cv2.imread(file.get_file_path())
            image = cv2.resize(image,(150,150))
            cv2.imwrite(cache_path,image)
        with open(cache_path,'rb') as f:
            byte = f.read()
        return HttpResponse(byte)

@login_required
def folder_show(request, path):
    if request.method == 'GET':
        path = urlunquote(path.strip('/'))
        if path == "":
            return redirect("/netdisk/folder/root")

        basedir = get_object_or_404(Folder, path=path)
        folder = Folder.objects.filter(parent=basedir.path)
        files = File.objects.filter(dir=basedir)
        path_link = path_to_link(path)
        context = {'folders': folder, 'files': files, 'path':path,'path_link':path_link}
        return render(request, "netdisk/folder.html", context)

@login_required
def create(request,path):
    if request.method == 'POST':
        parent = get_object_or_404(Folder,path=path)
        name = request.POST.get("folder_name")
        if not name:
            return HttpResponse("文件夹名称不能为空")
        folder_list = Folder.objects.filter(parent=parent)
        unique_name = get_unique_folder_name(name, folder_list)
        path = "/".join([path, unique_name])
        Folder.objects.create(name=unique_name, path=path, parent=parent)
        return redirect('/netdisk/folder/' + parent.path)


@login_required
def rename(request, type, path):
    if request.method == 'POST':
        if type == 'folder':
            obj = Folder.objects.get(path=path)
            name = request.POST.get("new_name")
            if obj.name != name:
                folder_list = Folder.objects.filter(parent=obj.parent)
                unique_name = get_unique_folder_name(name, folder_list)
                obj.name = unique_name
                obj.path = "/".join([os.path.dirname(path), unique_name])
                obj.save()
            message = "文件夹：{}重命名为{}".format(path, obj.path)
        elif type == 'file':
            name = os.path.basename(path)
            new_name = request.POST.get("new_name")
            print(f"new_name: {new_name}")
            print(f"name: {name}")
            if new_name != name:
                suffix = os.path.splitext(name)[1]
                dir = os.path.dirname(path)
                file = get_object_or_404(File, name=name, dir__path=dir)

                if not os.path.splitext(new_name)[1]:
                    new_name += suffix

                file_list = File.objects.filter(dir=file.dir)
                new_name = get_unique_folder_name(new_name, file_list)
                file.name = get_unique_folder_name(new_name, file_list)
                file.save()
                message = "文件：{}重命名为{}".format(name, new_name)
        return render(request, 'netdisk/pageJump.html', {'message':message})

@login_required
def delete(request, type, path):
    if request.method == 'GET':
        if type =='folder':
            obj = Folder.objects.get(path=path)
            obj.remove()    # 删除文件夹及其所有子文件夹与文件
            message = "文件夹：{}删除成功".format(path)
        elif type == 'file':
            name = os.path.basename(path)
            dir = os.path.dirname(path)
            file = get_object_or_404(File, name=name,dir__path=dir)
            # 使用Link.minus_link删除一条连接以对应的一条文件数据
            Link.minus_link(file)
            message = "文件：{} 删除成功".format(name)
        return render(request, 'netdisk/pageJump.html', {'message':message})


@login_required
def prev_folder(request):
    if request.method == 'GET':
        back_path = os.path.dirname(request.META.get('HTTP_REFERER'))
        return redirect(back_path)


