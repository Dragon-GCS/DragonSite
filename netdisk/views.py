# Create your views here.
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .models import File, Folder, Link
from django.utils.http import urlunquote
import os
from django.contrib.auth.decorators import login_required
from .utils import handle_upload_files, get_unique_folder_name



@login_required
def index(request):
    return render(request, 'netdisk/test.html')

@login_required
def upload(request, path):
    files = request.FILES.getlist("files")
    parent = get_object_or_404(Folder, path=path)
    if not files:
        return render(request, 'netdisk/pageJump.html', {'message':'请选择文件'})
    else:
        handle_upload_files(files, parent)
        return render(request, 'netdisk/pageJump.html', {'message':'上传成功'})

@login_required
def download(request, path):
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
def folder_show(request, path):
    path = urlunquote(path.strip('/'))
    if path == "":
        return redirect("/netdisk/folder/root")

    basedir = get_object_or_404(Folder, path=path)
    folder = Folder.objects.filter(parent=basedir.path)
    files = File.objects.filter(dir=basedir)
    context = {'folders': folder, 'files': files, 'path':path}
    return render(request, "netdisk/folder.html", context)

@login_required
def create(request,path):
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
def delete(request, type, path):
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
    back_path = os.path.dirname(request.META.get('HTTP_REFERER'))
    return redirect(back_path)
