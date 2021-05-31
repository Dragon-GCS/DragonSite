# Create your views here.
from django.shortcuts import render,redirect
from django.db.utils import IntegrityError
from django.http import HttpResponse
from .models import File,Folder
from django.conf import settings
import os, re
from django.contrib.auth.decorators import login_required



@login_required
def index(request):
    return render(request, 'netdisk/test.html')

@login_required
def upload_file(request):
    request.session['page_from'] = request.META.get('HTTP_REFERER','/')
    print(request.session['page_from'])
    if request.method == 'POST':
        files = request.FILES.getlist("files")
        path =request.POST.get('path')
        parent = request.POST.get('parent')
        if not files:
            return render(request, 'netdisk/pageJump.html', {'message':'请选择文件'})
        else:
            for content in files:
                f_name = content.name
                save_path = os.path.join(settings.MEDIA_ROOT,parent,path)
                print(save_path)
                folder = Folder(folder_path=os.path.join(parent,path),folder_name=path,parent_folder_name=parent)
                if not os.path.exists(save_path):
                    os.makedirs(save_path)
                    folder.save()


                folder = Folder.objects.get(folder_path=os.path.join(parent,path))
                file = File(filename=f_name,file_path=folder)
                if not File.objects.filter(filename=f_name,file_path__folder_path=folder.folder_path):
                    with open(os.path.join(save_path,f_name),'wb+') as f:
                        for chunks in content.chunks():
                            f.write(chunks)
                    file.save()

            return render(request, 'netdisk/pageJump.html', {'message':'上传成功'})
    return render(request, 'netdisk/upload.html')#redirect(request.session['page_from'])

def folder_show(request, path):
    path = path.strip('/')
    if path == "":
        return redirect("/netdisk/folder/root")
    folder = Folder.objects.filter(parent=path)
    files = File.objects.filter(dir__path=path)
    if not Folder.objects.filter(path=path):
        return HttpResponse(path + '文件夹不存在')
    return render(request, 'netdisk/folder.html', {'folders':folder, 'files':files})

def create_folder(request):
    request.session['page_from'] = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        parent_folder_path = re.sub(r'.*/netdisk/folder/','',request.session['page_from'])
        folder_name = request.POST.get('folder_name')
        folder_path = '/'.join([parent_folder_path, folder_name])
        parent = Folder.objects.get(path=parent_folder_path)
        try:
            Folder.objects.create(name=folder_name, path=folder_path,parent=parent)
            return redirect('/netdisk/folder/'+parent_folder_path)
        except IntegrityError:
            return HttpResponse('File already exists')

def delete_folder(request,path):
    obj = Folder.objects.get(folder_path=path)
    obj.delete()
    return redirect(request.META.get('HTTP_REFERER'))

def back_folder(request):
    path = request.META.get('HTTP_REFERER').split('/')
    back_path = '/'.join(path[:-1])
    return redirect(back_path)
